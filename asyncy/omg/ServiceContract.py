# -*- coding: utf-8 -*-
from .OmgExceptions import OmgMismatchedPropertyLengthError, \
    OmgMissingKeyInBodyError, OmgPropertyKeyMissingTypeError, \
    OmgPropertyTypeNotFoundError, OmgPropertyValueMismatchError


class ServiceContract:

    @classmethod
    def ensure_value_of_type(cls, _type, value):
        """
        Ensures that the value matches the expected type as listed on
        https://microservice.guide/schema/actions/#arguments.

        Supported types: int, float, number, string, list, map, boolean, or any
        """
        if _type == 'string':
            cls.ensure_type(str, value, _type)
        elif _type == 'int':
            cls.ensure_type(int, value, _type)
        elif _type == 'boolean':
            cls.ensure_type(bool, value, _type)
        elif _type == 'map':
            cls.ensure_type(dict, value, _type)
        elif _type == 'float':
            cls.ensure_type(float, value, _type)
        elif _type == 'list':
            cls.ensure_type(list, value, _type)
        elif _type == 'number':
            cls.ensure_type_list([int, float], value, _type)
        elif _type == 'any':
            return
        else:
            raise OmgPropertyTypeNotFoundError(_type)

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
    def ensure_type(typ, val, _type):
        """
        Check if value belongs to the type specified.
        """
        if isinstance(val, typ):
            return
        raise OmgPropertyValueMismatchError(_type, val)

    @staticmethod
    def ensure_type_list(_list, val, _type):
        """
        Check if value belongs to the type specified.
        """
        for item in _list:
            if isinstance(val, item):
                return
        raise OmgPropertyValueMismatchError(_type, val)
