import re
import shutil
import os.path
import logging
from io import BytesIO

from jinja2 import Template
from packy_agent.utils.misc import atomic_write

from packy_agent.utils.pkg_resources import get_package_file_content
from packy_agent.utils.misc import (get_operating_system, get_interfaces, UBUNTU_16_04_XENIAL,
                                    LINUXMINT_18_1_SERENA)
from packy_agent.configuration.control_server.base import configuration
from packy_agent.configuration.agent.base import configuration as agent_configuration
from packy_agent.utils.misc import run_shell_command_async
from packy_agent.utils.network import get_machine_ip_address


INTERFACES_CONFIG_PATH = '/etc/network/interfaces'
SUPPORTED_OPERATING_SYSTEMS = (UBUNTU_16_04_XENIAL, LINUXMINT_18_1_SERENA)
STATIC_TEMPLATE_TYPE = 'static'
DHCP_TEMPLATE_TYPE = 'dhcp'
OPERATING_SYSTEM_TEMPLATES = {
    UBUNTU_16_04_XENIAL: {STATIC_TEMPLATE_TYPE: 'templates/network/ubuntu/static',
                          DHCP_TEMPLATE_TYPE: 'templates/network/ubuntu/dhcp'},
    LINUXMINT_18_1_SERENA: {STATIC_TEMPLATE_TYPE: 'templates/network/ubuntu/static',
                            DHCP_TEMPLATE_TYPE: 'templates/network/ubuntu/dhcp'},
}
STANZA_RE = re.compile(r'^\s*(?:iface|mapping|auto|allow-\S+|source|source-directory)')
IFACE_STANZA_RE = re.compile(r'^\s*iface\s+(?P<iface>\S+)\s+inet\s+(?P<method>\S+)')
AUTO_STANZA_RE = re.compile(r'^\s*(auto|allow-auto)\s+(?P<iface>\S+)')


BACKUP_FILENAME_TEMPLATE = '{}.packy.backup'

ADDR_RE = {
    'ip_address': re.compile('\s*address\s+(\S+)'),
    'subnet_mask': re.compile('\s*netmask\s+(\S+)'),
    'default_gateway': re.compile('\s*gateway\s+(\S+)'),
    'name_servers': re.compile('\s*dns-nameservers\s+(.*)'),
}
ANY_SPACE_RE = re.compile('\s+')

logger = logging.getLogger(__name__)


def get_operating_system_template_path(template_type):
    operating_system = get_operating_system()
    return (OPERATING_SYSTEM_TEMPLATES.get(operating_system) or {}).get(template_type)


def update_network(interface, delay_seconds=0):
    run_shell_command_async('ip addr flush {interface}; '
                            'systemctl restart networking.service'.format(interface=interface),
                            delay_seconds=delay_seconds)


class NetworkManager(object):

    def __init__(self):

        self.stanzas = []
        self.interfaces_config_path = configuration.get_interfaces_config_path()

    def get_actual_ip_address(self):
        return get_machine_ip_address(agent_configuration.get_server_hostname())

    def read_network_configuration(self):
        stanzas = []

        lines = []
        stanzas.append(lines)
        with open(self.interfaces_config_path) as f:
            for line in f:
                match = STANZA_RE.match(line)
                if match:
                    lines = []
                    stanzas.append(lines)

                lines.append(line)

        self.stanzas = stanzas

    def get_stanza_by_interface(self, interface):
        for lines in self.stanzas:
            if lines:
                first_line = lines[0]
                match = IFACE_STANZA_RE.match(first_line)
                if match and match.group('iface') == interface:
                    return lines

    def get_current_configuration(self, interface):
        # TODO(dmu) MEDIUM: Implement more precise DHCP detection
        # We consider DHCP if interface is not configured in /etc/network/interfaces
        self.read_network_configuration()

        stanza = self.get_stanza_by_interface(interface)
        if not stanza:
            return {'dhcp': True}

        first_line = stanza[0]
        match = IFACE_STANZA_RE.match(first_line)
        if match.group('method') == 'dhcp':
            return {'dhcp': True}

        result = {'dhcp': False}

        for line in stanza:
            for k, regex in ADDR_RE.iteritems():
                match = regex.match(line)
                if match:
                    result[k] = match.group(1)

        name_servers = result.get('name_servers')
        if name_servers is not None:
            result['name_servers'] = ','.join(ANY_SPACE_RE.split(name_servers.strip()))

        return result

    def is_operating_system_supported(self):
        return get_operating_system() in SUPPORTED_OPERATING_SYSTEMS

    def get_configurable_network_interface(self):
        explicit_interface = configuration.get_network_interface()
        if explicit_interface:
            return explicit_interface

        interfaces = set(get_interfaces()) - {'lo'}
        interfaces = filter(lambda x: ':' not in x, interfaces)
        if len(interfaces) == 1:
            return interfaces[0]

    def backup_network_configuration(self):
        if os.path.isfile(self.interfaces_config_path):
            directory = os.path.dirname(self.interfaces_config_path)
            filename = BACKUP_FILENAME_TEMPLATE.format(
                os.path.basename(self.interfaces_config_path))
            backup_fullpath = os.path.join(directory, filename)
            if not os.path.isfile(backup_fullpath):
                shutil.copy(self.interfaces_config_path, backup_fullpath)

    def set_network(self, interface, template_path, context=None, update_network_delay_seconds=5):
        if not self.is_operating_system_supported():
            raise NotImplementedError('This operating system is not supported')

        self.read_network_configuration()

        template_text = get_package_file_content('packy_agent.configuration', template_path)

        template = Template(template_text)

        context = context or {}
        context['interface'] = interface
        content = '\n\n' + template.render(**context) + '\n\n'

        stream = BytesIO()

        written = False
        for lines in self.stanzas:
            if lines:
                first_line = lines[0]
                match = AUTO_STANZA_RE.match(first_line)
                if match:
                    stanza_iface = match.group('iface')
                    if stanza_iface == interface:
                        continue
                    else:
                        parts = stanza_iface.split(':')
                        if parts[0] == interface:
                            continue

                match = IFACE_STANZA_RE.match(first_line)
                if match:
                    stanza_iface = match.group('iface')
                    if stanza_iface == interface:
                        stream.write(content.encode('utf-8'))
                        written = True
                        continue
                    else:
                        parts = stanza_iface.split(':')
                        if parts[0] == interface:
                            # Skip virtual interfaces
                            continue

            for line in lines:
                stream.writelines(line)

        if not written:
            stream.write(content.encode('utf-8'))

        stream.seek(0)
        if configuration.is_network_configuration_enabled():
            self.backup_network_configuration()

            with atomic_write(self.interfaces_config_path, overwrite=True) as f:
                f.write(stream.read())
            run_shell_command_async('reboot now', delay_seconds=update_network_delay_seconds)
            # TODO(dmu) MEDIUM: Improve to change IP address without reboot (this includes proper restart
            #                   Packy Agent and Control Server to use update network settings
            # update_network(interface, delay_seconds=self.update_network_delay_seconds)
        else:
            logger.info('Network configuration change was disabled (for developer protection)')
            print 'Generated configuration file content:\n{}'.format(stream.read().decode('utf-8'))

    def set_static_ip_address(self, interface, ip_address, subnet_mask, default_gateway,
                              name_servers=('8.8.8.8', '8.8.4.4'), update_network_delay_seconds=5):
        context = {
            'ip_address': ip_address,
            'subnet_mask': subnet_mask,
            'default_gateway': default_gateway,
            'name_servers': name_servers,
        }
        self.set_network(interface, get_operating_system_template_path(STATIC_TEMPLATE_TYPE),
                         context=context, update_network_delay_seconds=update_network_delay_seconds)

    def set_dhcp(self, interface, update_network_delay_seconds=5):
        self.set_network(interface, get_operating_system_template_path(DHCP_TEMPLATE_TYPE),
                         update_network_delay_seconds=update_network_delay_seconds)


network_manager = NetworkManager()
