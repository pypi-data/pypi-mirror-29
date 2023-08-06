class ServiceBase(object):

    def __init__(self, name):
        self.name = name

    def start(self):
        raise NotImplementedError('Must be implemented in child class')

    def stop(self):
        raise NotImplementedError('Must be implemented in child class')

    def restart(self):
        raise NotImplementedError('Must be implemented in child class')

    def is_running(self):
        raise NotImplementedError('Must be implemented in child class')
