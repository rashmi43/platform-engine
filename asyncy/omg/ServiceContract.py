# -*- coding: utf-8 -*-
from .OmgExceptions import OmgMismatchedPropertyLengthError, \
    OmgMissingKeyInBodyError, OmgPropertyKeyMissingTypeError, \
    OmgPropertyValueMismatchError


class ServiceContract:

    @classmethod
    def ensure_value_of_type(cls, _type, value):
        """
        Ensures that the value matches the expected type as listed on
        https://microservice.guide/schema/actions/#arguments.

        Supported types: int, float, string, list, map, boolean, or any
        """
        if _type == 'string':
            cls.ensure_type(str, value)
        if _type == 'int':
            cls.ensure_type(int, value)
        if _type == 'boolean':
            cls.ensure_type(bool, value)
        if _type == 'map':
            cls.ensure_type(dict, value)
        if _type == 'float':
            cls.ensure_type(float, value)
        if _type == 'list':
            cls.ensure_type(list, value)
        if _type == 'number':
            cls.ensure_type_list([int, float], value, _type)
        if _type == 'any':
            return

    @classmethod
    def validate_output_properties(cls, output: dict, body, story,
                                   line):
        """
        Verify all properties are contained in the return body
        """
        if (not body and output) or (not output and body):
            raise OmgMismatchedPropertyLengthError(len(output), len(body))
        props = output.get('properties')
        if len(props) != len(body):
            raise OmgMismatchedPropertyLengthError(len(props), len(body))
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
    def ensure_type(typ, val):
        """
        Check if value belongs to the type specified.
        """
        if isinstance(val, typ):
            return
        raise OmgPropertyValueMismatchError(typ, val)

    @staticmethod
    def ensure_type_list(_list, val, _type):
        """
        Check if value belongs to the type specified.
        """
        for item in _list:
            if isinstance(val, item):
                return
        raise OmgPropertyValueMismatchError(_type, val)
