import logging
import os
import os.path
import yaml
import stat

from packy_agent.utils.misc import atomic_write


logger = logging.getLogger(__name__)


class BaseConfiguration(object):

    PACKY_CONFIGURATION_KEY = 'packy'

    def __init__(self):
        self.common_configuration = None
        self.local_configuration = {}
        self.local_configuration_mtime = None

    def get_local_configuration_file_path(self):
        raise NotImplementedError('Method must be implemented by child classes')

    def load_local_configuration(self, content=None, force=False):
        if content is not None:
            self.local_configuration = yaml.load(content)
            return True

        file_path = self.get_local_configuration_file_path()
        if not os.path.isfile(file_path):
            logger.debug('Configuration file %s does not exist', file_path)
            self.local_configuration.clear()
            self.local_configuration_mtime = None
            return True

        # TODO(dmu) LOW: Because we write to configuration file during run time it potentially
        #                may disappear at this point (if we delete it).
        #                Consider handling this situation
        mtime = os.path.getmtime(file_path)
        if mtime == self.local_configuration_mtime and not force:
            return False

        with open(file_path) as f:
            self.local_configuration = yaml.load(f)

        self.local_configuration_mtime = mtime
        return True

    def save_local_configuration(self, content=None):
        if content is None:
            config_yaml = yaml.safe_dump(dict(self.local_configuration), default_flow_style=False)
        else:
            if isinstance(content, basestring):
                yaml.load(content)  # for basic validation
                config_yaml = content
            else:
                config_yaml = yaml.safe_dump(content, default_flow_style=False)

        local_configuration_file_path = self.get_local_configuration_file_path()
        dir_path = os.path.dirname(local_configuration_file_path)
        if not os.path.isdir(dir_path):
            raise Exception('Directory for configuration file does not exist: {}'.format(dir_path))

        logger.debug('Saving local configuration to %s', local_configuration_file_path)
        with atomic_write(local_configuration_file_path, overwrite=True) as f:
            f.write(config_yaml)

        # TODO(dmu) MEDIUM: Consider not doing chmod, but it is convenient for development now
        os.chmod(local_configuration_file_path,
                 stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH |
                 stat.S_IWOTH)

    def is_debug_mode(self):
        return os.getenv('PACKY_AGENT_DEBUG', '').lower() in ('1', 'y', 'yes', 'true')
