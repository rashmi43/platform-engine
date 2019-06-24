# -*- coding: utf-8 -*-
from ..Exceptions import AsyncyError, OmgPropertyTypeMissingError, \
    OmgPropertyValueMismatchError


class ServiceContract:

    @classmethod
    def check_value_with_type(cls, typ, value):
        """
        Validates for types listed on
        https://microservice.guide/schema/actions/#arguments.

        Supported types: int, float, string, list, map, boolean, or any
        """
        if typ is None:
            raise OmgPropertyTypeMissingError(typ)
        if typ == 'string':
            cls.check_types(str, value)
        if typ == 'int':
            cls.check_types(int, value)
        if typ == 'boolean':
            cls.check_types(bool, value)
        if typ == 'map':
            cls.check_types(dict, value)
        if typ == 'float':
            cls.check_types(float, value)
        if typ == 'list':
            cls.check_types(list, value)
        if typ == 'any':
            return

    @classmethod
    def validate_output_properties(cls, output: dict, body, story,
                                   line):
        """
        Verify all properties are contained in the return body
        """
        # if body is None or {}:
        #    return
        if output is None or {}:
            return
        props = output.get('properties')
        for key in props:
            if key not in body:
                raise AsyncyError(message=f'Output contract violated! '
                                  f'Property key not found: {key}; '
                                  f'Expected key is missing in return ',
                                  story=story, line=line)
            elif props.get(key).get('type') == 'object':
                cls.validate_output_properties(
                    props.get(key), body.get(key), story, line)
            else:
                cls.check_value_with_type(
                    props.get(key).get('type'), body[key])

    @staticmethod
    def check_types(typ, val):
        """
        Resolves a string to itself. If values are given, the string
        is formatted against data, using the order in values.
        """
        if isinstance(val, typ):
            return
        raise OmgPropertyValueMismatchError(typ, val)
