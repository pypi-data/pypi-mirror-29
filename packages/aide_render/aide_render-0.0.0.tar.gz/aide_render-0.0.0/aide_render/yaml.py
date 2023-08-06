"""aide_render's YAML decomposition logic. aide_render uses standard pyYaml with
additional tags supported. Here's a list of the currently supported tags and
their use case:
  * !u: used with a unit string (ie: 5 meter) to represent a pint quantity.
"""

from yaml import *
from aide_design.units import unit_registry as u
import re

def units_representer(dumper, data):
    return dumper.represent_scalar(u'!u', str(data))


add_representer(u.Quantity, units_representer)


def units_constructor(loader, node):
    value = loader.construct_scalar(node)
    mag, units = value.split(' ')
    return u.Quantity(float(mag), units)


add_constructor(u'!u', units_constructor)


#resolve units implicitly:
pattern = re.compile(r'[+-]?([0-9]*[.])?[0-9]+[ ]([A-z]+[/*]*[0-9]*)')
add_implicit_resolver(u'!u', pattern)