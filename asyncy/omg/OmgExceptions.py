# -*- coding: utf-8 -*-


class AsyncyError(Exception):

    def __init__(self, message=None, story=None, line=None):
        super().__init__(message)
        self.message = message
        self.story = story
        self.line = line


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
    Raised when response body does not contain
    the key from microservice.yml
    """
    def __init__(self, prop_len, body_len):
        super().__init__(
            f'The number of properties in the microservice.yml {prop_len} '
            'does not match the number of items returned by the body '
            f'{body_len}. Please make sure your microservice returns all'
            ' the properties.')
        self.prop_len = prop_len
        self.body_len = body_len


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
        self.typ = _type


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
