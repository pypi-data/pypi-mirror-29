from __future__ import absolute_import
import json


from schematics import Model


class CustomModel(Model):

    def to_json(self, *args, **kwargs):
        return json.dumps(self.to_primitive(*args, **kwargs))
