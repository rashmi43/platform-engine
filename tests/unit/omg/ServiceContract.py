# -*- coding: utf-8 -*-
import json
import uuid
from unittest.mock import MagicMock, Mock

from asyncy.omg.OmgExceptions import OmgMismatchedPropertyLengthError, \
    OmgMissingKeyInBodyError, OmgPropertyKeyMissingTypeError, \
    OmgPropertyValueMismatchError
from asyncy.omg.ServiceContract import ServiceContract

import pytest
from pytest import mark, raises

from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse


def test_validate_output_properties(story):
    line = {}
    command_conf = {
        'output': {
            'type': 'object',
            'contentType': 'application/json',
            'properties': {
                'msg_id': {
                    'help': 'The message ID',
                    'type': 'int'
                },
                'from': {
                    'help': 'The object with bot details.',
                    'type': 'string'
                },
                'chat': {
                    'help': 'The chat object with chat details.',
                    'type': 'string'
                },
                'id': {
                    'type': 'object',
                    'properties': {
                        'cid': {
                            'type': 'int'
                        },
                        'cmsg': {
                            'type': 'string'
                        }
                    }
                }
            }
        }
    }
    body = '{"from": "storyscript", "msg_id": 123, "chat": "chat", \
             "id": {"cid": 111, "cmsg": "hello"}}'

    ServiceContract.validate_output_properties(
        command_conf.get('output'), json.loads(body), story, line)


def test_validate_output_properties_triple_nested(story):
    line = {}
    command_conf = {
        'output': {
            'type': 'object',
            'contentType': 'application/json',
            'properties': {
                'msg_id': {
                    'help': 'The message ID',
                    'type': 'int'
                },
                'from': {
                    'help': 'The object with bot details.',
                    'type': 'string'
                },
                'chat': {
                    'help': 'The chat object with chat details.',
                    'type': 'string'
                },
                'id': {
                    'type': 'object',
                    'properties': {
                        'cid': {
                            'type': 'int'
                        },
                        'cmsg': {
                            'type': 'object',
                            'properties': {
                                'name': {
                                    'type': 'string'
                                },
                                'cmsg_id': {
                                    'type': 'int'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    body = '{"from": "storyscript", "msg_id": 123, "chat": "chat", \
             "id": {"cid": 111, "cmsg": {"name": "ss", "cmsg_id": 1}}}'

    ServiceContract.validate_output_properties(
        command_conf.get('output'), json.loads(body), story, line)


def test_validate_output_properties_body_none(story):
    line = {}
    command_conf = {
        'output': {
            'type': 'object',
            'contentType': 'application/json',
            'properties': {
                'msg_id': {
                    'help': 'The message ID',
                    'type': 'int'
                }
            }
        }
    }
    body = {}
    message = 'The number of properties in the microservice.yml 3 does not' \
        ' match the number of items returned by the body 0. Please make sure' \
        ' your microservice returns all the properties.'

    with pytest.raises(OmgMismatchedPropertyLengthError, match=message):
        ServiceContract.validate_output_properties(
            command_conf.get('output'), body, story, line)


def test_validate_output_properties_type_number_mismatch(story):
    line = {}
    command_conf = {
        'output': {
            'type': 'object',
            'contentType': 'application/json',
            'properties': {
                'msg_id': {
                    'help': 'The message ID',
                    'type': 'number'
                }
            }
        }
    }
    body = {'msg_id': '1.9'}
    message = 'The property value 1.9 should be of type number. '\
        'It does not adhere to the microservice service contract.'

    with pytest.raises(OmgPropertyValueMismatchError, match=message):
        ServiceContract.validate_output_properties(
            command_conf.get('output'), body, story, line)


def test_validate_output_properties_type_number(story):
    line = {}
    command_conf = {
        'output': {
            'type': 'object',
            'contentType': 'application/json',
            'properties': {
                'msg_id': {
                    'help': 'The message ID',
                    'type': 'number'
                }
            }
        }
    }
    body = {'msg_id': 1.9}

    ServiceContract.validate_output_properties(
        command_conf.get('output'), body, story, line)


def test_validate_output_properties_missing_type(story):
    line = {}
    command_conf = {
        'output': {
            'type': 'object',
            'contentType': 'application/json',
            'properties': {
                'msg_id': {
                    'help': 'The message ID',
                }
            }
        }
    }
    body = {'msg_id': 123}
    message = 'The property msg_id does not have a type specifed. ' \
        'Please check microservice.yml and specify type for each value.'

    with pytest.raises(OmgPropertyKeyMissingTypeError, match=message):
        ServiceContract.validate_output_properties(
            command_conf.get('output'), body, story, line)


def test_validate_output_properties_output_none(story):
    line = {}
    command_conf = {
        'output': {}
    }
    body = '{"abc": "def"}'
    message = 'The number of properties in the microservice.yml 0 does not' \
        ' match the number of items returned by the body 1. Please make' \
        ' sure your microservice returns all the properties.'

    with pytest.raises(OmgMismatchedPropertyLengthError, match=message):
        ServiceContract.validate_output_properties(
            command_conf.get('output'), json.loads(body), story, line)


def test_validate_output_properties_missing_property_key(story):
    command_conf = {
        'output': {
            'type': 'object',
            'contentType': 'application/json',
            'properties': {
                'msg_id': {
                    'help': 'The message ID',
                    'type': 'int'
                },
                'from': {
                    'help': 'The object with bot details.',
                    'type': 'string'
                },
                'id': {
                    'help': 'The chat object with chat details.',
                    'type': 'string'
                }
            }
        }
    }
    body = '{"from": "storyscript", "msg_id": 123, "chat": "my chat"}'
    message = 'Output contract violated. The property id is not found in the' \
              ' response body. Please make sure your microservice returns' \
              ' this.'

    with pytest.raises(OmgMissingKeyInBodyError, match=message):
        ServiceContract.validate_output_properties(
            command_conf.get('output'), json.loads(body), story, {})


@mark.parametrize('body', [{'message_id': 'msg_id_1', 'status': False},
                           {'message_id': '123', 'status': True},
                           {'status': True, 'message_id': '123'}])
def test_validate_output_properties_mismatched_property(body, story):
    command_conf = {
        'output': {
            'type': 'object',
            'contentType': 'application/json',
            'properties': {
                'message_id': {
                    'help': 'The message ID',
                    'type': 'int'
                },
                'status': {
                    'type': 'boolean',
                    'help': 'status'
                }
            }
        }
    }
    val = body['message_id']
    message = f'The property value {val} should be of type <class \'int\'>.' \
              f' It does not adhere to the microservice service contract.'

    with pytest.raises(OmgPropertyValueMismatchError, match=message):
        ServiceContract.validate_output_properties(
            command_conf.get('output'), body, story, {})


@mark.parametrize('body', ['{"message_id1": "msg_id_1", "status": "False"}',
                           '{"to": "123", "status": "True"}',
                           '{"status": "True", "message_id1": "123"}'])
def test_validate_output_properties_missing_property(body, story):
    command_conf = {
        'output': {
            'type': 'object',
            'contentType': 'application/json',
            'properties': {
                'message_id': {
                    'help': 'The message ID',
                    'type': 'int'
                },
                'status': {
                    'type': 'boolean',
                    'help': 'status'
                }
            }
        }
    }
    message = 'Output contract violated. The property message_id is ' \
              'not found in the response body. Please make sure your' \
              ' microservice returns this.'

    with pytest.raises(OmgMissingKeyInBodyError, match=message):
        ServiceContract.validate_output_properties(
            command_conf.get('output'), json.loads(body), story, {})


@mark.parametrize('typ,val', [('int', 1), ('float', 0.9), ('string', 'hello'),
                              ('list', [0, 1]), ('map', {'a': 'b'}),
                              ('boolean', True), ('any', False)])
def test_check_value_each_type(typ, val, story):
    ServiceContract.ensure_value_of_type(typ, val)


@mark.parametrize('typ,val', [('int', 1.9), ('float', 1), ('string', 1),
                              ('list', 'hello'), ('map', [0, 1]),
                              ('boolean', 'True')])
def test_fail_check_value_each_type(typ, val, story):
    msg = f'The property value {val} should be of type {typ}.It does \
        not adhere to the microservice service contract.'
    with pytest.raises(OmgPropertyValueMismatchError):
            ServiceContract.ensure_value_of_type(typ, val) == msg
