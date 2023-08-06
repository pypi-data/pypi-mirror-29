import flask
from flask.views import MethodView

from packy_agent.control_server.forms.network import NetworkForm
from packy_agent.configuration.control_server.base import configuration
from packy_agent.managers.network import network_manager
from packy_agent.control_server.views.base import smart_redirect
from packy_agent.utils.auth import activation_and_authentication_required


DELAY_SECONDS = 5


class NetworkView(MethodView):

    def get_form_context(self):
        is_operating_system_supported = network_manager.is_operating_system_supported()
        network_interface = network_manager.get_configurable_network_interface()

        if is_operating_system_supported and network_interface:
            form_kwargs = network_manager.get_current_configuration(network_interface)
            form_kwargs['network_interface'] = network_interface
            form = NetworkForm(**form_kwargs)
        else:
            form = None

        context = {
            'form': form,
            'is_network_configuration_enabled': configuration.is_network_configuration_enabled(),
            'is_operating_system_supported': is_operating_system_supported,
            'network_interface': network_interface,
            'active_menu_item': 'network',
        }
        return context

    @activation_and_authentication_required
    def get(self):
        context = self.get_form_context()
        return flask.render_template('network.html', **context)

    @activation_and_authentication_required
    def post(self):
        form = NetworkForm()
        if form.validate():
            if form.dhcp.data:
                network_manager.set_dhcp(interface=form.network_interface.data)
            else:
                kwargs = dict(
                    ip_address=form.ip_address.data,
                    subnet_mask=form.subnet_mask.data,
                    default_gateway=form.default_gateway.data,
                    interface=form.network_interface.data
                )
                if form.name_servers.data:
                    kwargs['name_servers'] = form.name_servers.data.split(',')
                network_manager.set_static_ip_address(**kwargs)

            if configuration.is_network_configuration_enabled():
                flask.flash('Operation will start in {} seconds...'.format(DELAY_SECONDS))
            else:
                flask.flash('Please, see logs for more information')

            return smart_redirect('success', 'network')

        context = self.get_form_context()
        context['form'] = form
        return flask.render_template('network.html', **context)
