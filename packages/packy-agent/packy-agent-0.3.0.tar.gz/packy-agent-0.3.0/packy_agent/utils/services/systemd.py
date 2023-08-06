import os
import stat

from packy_agent.utils.services.base import ServiceBase
from packy_agent.utils.shell import run_command
from packy_agent.utils.output import write_to_console_or_file


class SystemdService(ServiceBase):

    RELOAD_SYSTEMD_CONFIGURATION_COMMAND = 'systemctl daemon-reload'
    MAKE_START_ON_REBOOT_COMMAND_TEMPLATE = 'update-rc.d {name} defaults'
    ENABLE_UNIT_SERVICE_COMMAND_TEMPLATE = 'systemctl enable {name}.service'
    IS_ACTIVE_SERVICE_COMMAND_TEMPLATE = 'systemctl is-active {name}.service'

    START_COMMAND_TEMPLATE = 'service {name} start'
    STOP_COMMAND_TEMPLATE = 'service {name} stop'
    RESTART_COMMAND_TEMPLATE = 'service {name} restart'
    RELOAD_COMMAND_TEMPLATE = 'service {name} reload'

    SYSTEMCTL_START_COMMAND_TEMPLATE = 'systemctl start {name}.service'
    SYSTEMCTL_STOP_COMMAND_TEMPLATE = 'systemctl stop {name}.service'
    SYSTEMCTL_RESTART_COMMAND_TEMPLATE = 'systemctl restart {name}.service'
    SYSTEMCTL_RELOAD_COMMAND_TEMPLATE = 'systemctl reload {name}.service'

    INITD_PATH_TEMPLATE = '/etc/init.d/{name}'
    # TODO(dmu) MEDIUM: Is `UNIT_SERVICE_PATH_TEMPLATE` different on OSes other than Ubuntu
    UNIT_SERVICE_PATH_TEMPLATE = '/lib/systemd/system/{name}.service'

    def __init__(self, name):
        super(SystemdService, self).__init__(name)

        self.start_command = self.START_COMMAND_TEMPLATE.format(name=name)
        self.stop_command = self.STOP_COMMAND_TEMPLATE.format(name=name)
        self.restart_command = self.RESTART_COMMAND_TEMPLATE.format(name=name)
        self.reload_command = self.RELOAD_COMMAND_TEMPLATE.format(name=name)

        self.systemctl_start_command = self.SYSTEMCTL_START_COMMAND_TEMPLATE.format(name=name)
        self.systemctl_stop_command = self.SYSTEMCTL_STOP_COMMAND_TEMPLATE.format(name=name)
        self.systemctl_restart_command = self.SYSTEMCTL_RESTART_COMMAND_TEMPLATE.format(name=name)
        self.systemctl_reload_command = self.SYSTEMCTL_RELOAD_COMMAND_TEMPLATE.format(name=name)

        self.make_start_on_reboot_command = self.MAKE_START_ON_REBOOT_COMMAND_TEMPLATE.format(
            name=name)
        self.enable_unit_service_command = self.ENABLE_UNIT_SERVICE_COMMAND_TEMPLATE.format(
            name=name)
        self.is_active_service_command = self.IS_ACTIVE_SERVICE_COMMAND_TEMPLATE.format(name=name)

        self.initd_path = self.INITD_PATH_TEMPLATE.format(name=name)
        self.unit_service_path = self.UNIT_SERVICE_PATH_TEMPLATE.format(name=name)

    @classmethod
    def reload_systemd_configuration(cls, raise_exception=False):
        run_command(cls.RELOAD_SYSTEMD_CONFIGURATION_COMMAND, raise_exception=raise_exception)

    def start(self, systemctl=False, raise_exception=False):
        command = self.systemctl_start_command if systemctl else self.start_command
        run_command(command, raise_exception=raise_exception)

    def stop(self, systemctl=False, raise_exception=False):
        command = self.systemctl_stop_command if systemctl else self.stop_command
        run_command(command, raise_exception=raise_exception)

    def restart(self, systemctl=False, raise_exception=False):
        command = self.systemctl_restart_command if systemctl else self.restart_command
        run_command(command, raise_exception=raise_exception)

    def reload(self, systemctl=False, raise_exception=False):
        command = self.systemctl_reload_command if systemctl else self.reload_command
        run_command(command, raise_exception=raise_exception)

    def make_start_on_reboot(self, raise_exception=False):
        run_command(self.make_start_on_reboot_command, raise_exception=raise_exception)

    def enable_unit_service(self, raise_exception=False):
        run_command(self.enable_unit_service_command, raise_exception=raise_exception)

    def update_initd_script(self, content):
        initd_path = self.initd_path
        write_to_console_or_file(initd_path, content)
        os.chmod(initd_path, os.stat(initd_path).st_mode | stat.S_IEXEC)
        packy_service.reload_systemd_configuration(raise_exception=True)
        packy_service.make_start_on_reboot(raise_exception=True)

    def update_unit_service_configuration(self, content):
        write_to_console_or_file(self.unit_service_path, content)
        self.enable_unit_service(raise_exception=True)
        self.reload_systemd_configuration(raise_exception=True)
        self.restart(systemctl=True, raise_exception=True)

    def is_active(self, raise_exception=False):
        output = run_command(self.is_active_service_command, raise_exception=raise_exception)
        return output == 'active'


packy_service = SystemdService('packy')
nginx_service = SystemdService('nginx')
log2ram_service = SystemdService('log2ram')
