from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField
from wtforms import validators


class CommaSeparatedIPAddresses(validators.IPAddress):
    def __call__(self, form, field):
        value = field.data
        valid = False
        if value:
            for ip_address in value.split(','):
                ip_address = ip_address.strip()
                valid = ((self.ipv4 and self.check_ipv4(ip_address)) or
                         (self.ipv6 and self.check_ipv6(ip_address)))

        if not valid:
            message = self.message
            if message is None:
                message = field.gettext('Invalid IP address.')
            raise validators.ValidationError(message)


class NetworkForm(FlaskForm):

    dhcp = BooleanField('Use DHCP')
    ip_address = StringField('IP Address', validators=[validators.Optional(),
                                                       validators.IPAddress()])
    subnet_mask = StringField('Subnet Mask', validators=[validators.Optional(),
                                                         validators.IPAddress()])
    default_gateway = StringField('Default Gateway', validators=[validators.Optional(),
                                                                 validators.IPAddress()])
    name_servers = StringField('Name Servers', validators=[validators.Optional(),
                                                           CommaSeparatedIPAddresses()])

    network_interface = HiddenField()

    def validate(self):
        rv = super(NetworkForm, self).validate()
        if not rv:
            return False

        is_valid = True
        if not self.dhcp.data:
            for field in (self.ip_address, self.subnet_mask, self.default_gateway):
                if not field.raw_data or not field.raw_data[0]:
                    field.errors.append(field.gettext('This field is required.'))
                    is_valid = False

        return is_valid
