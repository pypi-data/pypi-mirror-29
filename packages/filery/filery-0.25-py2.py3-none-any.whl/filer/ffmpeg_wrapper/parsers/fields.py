#!/usr/bin/env python
from marshmallow.fields import Str


class ASCII(Str):
    def _deserialize(self, value, attr, data):
        if not isinstance(value, basestring):
            self.fail('invalid')
        return str(value)