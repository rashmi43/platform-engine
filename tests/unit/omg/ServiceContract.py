# -*- coding: utf-8 -*-
import json
import uuid
from unittest.mock import MagicMock, Mock

from asyncy.Exceptions import AsyncyError, OmgPropertyValueMismatchError
from asyncy.omg.ServiceContract import ServiceContract

import pytest
from pytest import mark

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
    body = '{"from": "storyscript", "msg_id": 123, "chat": "my chat"}'
    body1 = '{"from": "storyscript", "msg_id": 123, "chat": "chat", \
             "id": {"cid": 111, "cmsg": "hello"}}'
    message = 'Output contract violated! Property key not found: id; \
        Expected key is missing in return'

    ServiceContract.validate_output_properties(
        command_conf.get('output'), json.loads(body1), story, line)
    with pytest.raises(AsyncyError):
        ServiceContract.validate_output_properties(
            command_conf.get('output'), json.loads(body), story, {}) == message


@mark.parametrize('body', [{'message_id': 'msg_id_1'},
                           {'message_id': '123'},
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
    message = f'The property value message_id should be of type int.It does \
        not adhere to the microservice service contract.'

    with pytest.raises(OmgPropertyValueMismatchError):
        ServiceContract.validate_output_properties(
            command_conf.get('output'), body, story, {}) == message


@mark.parametrize('body', [{'message_id1': 'msg_id_1'},
                           {'to': 123},
                           {'status': True, 'message_id1': 123}])
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
    message = 'Output contract violated! Property key not found: message_id; \
        Expected key is missing in return'

    with pytest.raises(AsyncyError):
        ServiceContract.validate_output_properties(
            command_conf.get('output'), body, story, {}) == message


@mark.parametrize('typ,val', [('int', 1), ('float', 0.9), ('string', 'hello'),
                              ('list', [0, 1]), ('map', {'a': 'b'}),
                              ('boolean', True), ('any', False)])
def test_check_value_each_type(typ, val, story):
    ServiceContract.check_value_with_type(typ, val)


@mark.parametrize('typ,val', [('int', 1.9), ('float', 1), ('string', 1),
                              ('list', 'hello'), ('map', [0, 1]),
                              ('boolean', 'True')])
def test_fail_check_value_each_type(typ, val, story):
    msg = f'The property value {val} should be of type {typ}.It does \
        not adhere to the microservice service contract.'
    with pytest.raises(OmgPropertyValueMismatchError):
            ServiceContract.check_value_with_type(typ, val) == msg
