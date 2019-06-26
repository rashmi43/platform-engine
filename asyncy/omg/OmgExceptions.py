# -*- coding: utf-8 -*-
from ..Exceptions import AsyncyError


class OmgPropertyTypeNotFoundError(AsyncyError):
    """
    Raised when an unknown type is specified which is not
    recognised as per the OMG specification.
    """
    def __init__(self, _type):
        super().__init__(
            f'The property type {_type} is not supported.'
            ' Please specify a known type as per OMG specs.')
        self._type = _type


class OmgMissingKeyInBodyError(AsyncyError):
    """
    Raised when response body does not contain
    the key from microservice.yml
    """
    def __init__(self, key):
        super().__init__(
            f'Output contract violated. The property {key}'
            ' is not found in the response body.'
            ' Please make sure your microservice returns this.')
        self.key = key


class OmgMismatchedPropertyLengthError(AsyncyError):
    """
    Raised when either output is empty and body returns values
    or vice versa.
    """
    def __init__(self, props, body):
        super().__init__(
            f'The number of properties in the microservice.yml {len(props)} '
            'does not match the number of items returned by the body '
            f'{len(body)}. Please make sure your microservice returns all the'
            f' properties. The items are {props.keys()} and {body.keys()}')
        self.prop = props
        self.body = body


class OmgPropertyValueMismatchError(AsyncyError):
    """
    Raised when the property type from microservice.yml does not match
    the value type in the response body.
    """
    def __init__(self, _type, value):
        super().__init__(
            f'The property value {value} should be of type {_type}. '
            'It does not adhere to the microservice service contract.')
        self.value = value
        print(f'val is {value}')
        self._type = _type


class OmgPropertyKeyMissingTypeError(AsyncyError):
    """
    Raised when there is a microservice property does not have a
    type specified.
    """
    def __init__(self, key):
        super().__init__(
            f'The property {key} does not have a type specifed. '
            'Please check microservice.yml and specify type for each value.')
        self.key = key
