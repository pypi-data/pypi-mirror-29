"""
This module defines common converter keys, used by consumers of the
converter layer to identify the desired conversion type when querying a
:py:class:`uplink.converters.ConverterFactoryRegistry`.
"""
# Standard library imports
import functools

# Local imports
from uplink.converters import interfaces

__all__ = [
    "CONVERT_TO_STRING",
    "CONVERT_TO_REQUEST_BODY",
    "CONVERT_FROM_RESPONSE_BODY",
    "Map",
    "Sequence"
]

#: Object to string conversion.
CONVERT_TO_STRING = 0

#: Object to request body conversion.
CONVERT_TO_REQUEST_BODY = 1

# Response body to object conversion.
CONVERT_FROM_RESPONSE_BODY = 2


class CompositeKey(object):
    """
    A utility class for defining composable converter keys.

    Arguments:
        converter_key: The enveloped converter key.
    """
    class ConverterUsingFunction(interfaces.Converter):
        def __init__(self, convert_function):
            self._convert = convert_function

        def convert(self, value):
            return self._convert(value)

    def __init__(self, converter_key):
        self._converter_key = converter_key

    def __eq__(self, other):
        if isinstance(other, CompositeKey) and type(other) is type(self):
            return other._converter_key == self._converter_key
        return False

    def convert(self, converter, value):  # pragma: no cover
        raise NotImplementedError

    def __call__(self, converter_registry):
        factory = converter_registry[self._converter_key]

        def factory_wrapper(*args, **kwargs):
            converter = factory(*args, **kwargs)
            convert_func = functools.partial(self.convert, converter)
            return self.ConverterUsingFunction(convert_func)

        return factory_wrapper


class Map(CompositeKey):
    """
    Object to mapping conversion.

    The constructor argument :py:data:`converter_key` details the type
    for the values in the mapping. For instance::

        # Key for conversion of an object to a mapping of strings.
        Map(CONVERT_TO_STRING)
    """
    def convert(self, converter, value):
        return dict((k, converter.convert(value[k])) for k in value)


class Sequence(CompositeKey):
    """
    Object to sequence conversion.

    The constructor argument :py:data:`converter_key` details the type
    for the elements in the sequence. For instance::

        # Key for conversion of an object to a sequence of strings.
        Sequence(CONVERT_TO_STRING)
    """
    def convert(self, converter, value):
        if isinstance(value, (list, tuple)):
            return list(map(converter.convert, value))
        else:
            return converter.convert(value)
