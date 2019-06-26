# -*- coding: utf-8 -*-
from .OmgExceptions import OmgMismatchedPropertyLengthError, \
    OmgMissingKeyInBodyError, OmgPropertyKeyMissingTypeError, \
    OmgPropertyValueMismatchError


class ServiceContract:
    """
    Class to verify service contract is not violated. The response body
    must include the same properties as specified in the microservice.yml.
    This class has methods to verify the same/
    """

    @classmethod
    def ensure_value_of_type(cls, type_, value):
        """
        Ensures that the value matches the expected type as listed on
        https://microservice.guide/schema/actions/#arguments.

        Supported types: int, float, number, string, list, map, boolean, or any
        """
        assert type_ in ['int', 'float', 'number', 'boolean', 'string',
                         'map', 'list', 'any']
        if type_ == 'string':
            cls.ensure_type(str, value, type_)
        elif type_ == 'int':
            cls.ensure_type(int, value, type_)
        elif type_ == 'boolean':
            cls.ensure_type(bool, value, type_)
        elif type_ == 'map':
            cls.ensure_type(dict, value, type_)
        elif type_ == 'float':
            cls.ensure_type(float, value, type_)
        elif type_ == 'list':
            cls.ensure_type(list, value, type_)
        elif type_ == 'number':
            cls.ensure_type_list([int, float], value, type_)
        elif type_ == 'any':
            return

    @classmethod
    def validate_output_properties(cls, output: dict, body, story,
                                   line):
        """
        Verify all properties are contained in the return body
        """
        if bool(body) ^ bool(output):
            raise OmgMismatchedPropertyLengthError(output, body)
        props = output.get('properties')
        if len(props) != len(body):
            story.logger.error(f'The property items {props.keys()} do not '
                               f'match the body item length {body.keys()}')
            raise OmgMismatchedPropertyLengthError(props, body)
        for key, val in props.items():
            if key not in body:
                raise OmgMissingKeyInBodyError(key)
            elif val.get('type') is None and val.get('type') != 'object':
                raise OmgPropertyKeyMissingTypeError(key)
            elif val.get('type') == 'object':
                cls.validate_output_properties(
                    val, body[key], story, line)
            else:
                cls.ensure_value_of_type(
                    val.get('type'), body[key])

    @staticmethod
    def ensure_type(typ, val, type_):
        """
        Check if value belongs to the type specified.
        """
        if isinstance(val, typ):
            return
        raise OmgPropertyValueMismatchError(type_, val)

    @staticmethod
    def ensure_type_list(list_, val, type_):
        """
        Check if value belongs to the type specified.
        """
        for item in list_:
            if isinstance(val, item):
                return
        raise OmgPropertyValueMismatchError(type_, val)
