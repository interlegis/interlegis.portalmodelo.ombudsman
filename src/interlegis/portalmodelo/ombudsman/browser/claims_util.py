# -*- coding=utf-8 -*-

from collections import OrderedDict
import rows

def import_from_dicts(counter):
    keys = ('label', 'count')
    t = rows.Table(fields=OrderedDict(
        [(keys[0], rows.fields.TextField),
         (keys[1], rows.fields.IntegerField)]
    ))
    for key, value in counter.items():
        t.append({keys[0]: key, keys[1]: value})
    return t
