# -*- coding: utf-8 -*-


class AsyncyError(Exception):

    def __init__(self, message=None, story=None, line=None):
        super().__init__(message)
        self.message = message
        self.story = story
        self.line = line


class AsyncyRuntimeError(AsyncyError):
    pass


class TypeAssertionRuntimeError(AsyncyRuntimeError):
    def __init__(self, type_expected, type_received, value):
        super().__init__(message=f'Incompatible type assertion: '
                                 f'Received {value} ({type_received}), but '
                                 f'expected {type_expected}')


class TypeValueRuntimeError(AsyncyRuntimeError):
    def __init__(self, type_expected, type_received, value):
        super().__init__(message=f'Type conversion failed from '
                                 f'{type_received} to '
                                 f'{type_expected} with `{value}`')


class InvalidKeywordUsage(AsyncyError):
    def __init__(self, story, line, keyword):
        super().__init__(message=f'Invalid usage of keyword "{keyword}".',
                         story=story, line=line)


class ContainerSpecNotRegisteredError(AsyncyError):
    def __init__(self, container_name):
        super().__init__(message=f'Service {container_name} not registered!')


class TooManyVolumes(AsyncyError):
    def __init__(self, volume_count, max_volumes):
        super().__init__(
            message=f'Your app makes use of {volume_count} volumes. '
                    f'The total permissible limit during Asyncy Beta is '
                    f'{max_volumes} volumes. Please see '
                    f'https://docs.asyncy.com/faq/ for more information.')


class TooManyActiveApps(AsyncyError):
    def __init__(self, active_apps, max_apps):
        super().__init__(
            message=f'Only {max_apps} active apps are allowed during Asyncy '
                    f'Beta. Please see '
                    f'https://docs.asyncy.com/faq/ for more information.')


class TooManyServices(AsyncyError):
    def __init__(self, service_count, max_services):
        super().__init__(
            message=f'Your app makes use of {service_count} services. '
                    f'The total permissible limit during Asyncy Beta is '
                    f'{max_services} services. Please see '
                    f'https://docs.asyncy.com/faq/ for more information.')


class ArgumentNotFoundError(AsyncyError):

    def __init__(self, story=None, line=None, name=None):
        message = None
        if name is not None:
            message = name + ' is required, but not found'

        super().__init__(message, story=story, line=line)


class ArgumentTypeMismatchError(AsyncyError):

    def __init__(self, arg_name: str, omg_type: str, story=None, line=None):
        message = f'The argument "{arg_name}" does not match the expected ' \
                  f'type "{omg_type}"'
        super().__init__(message, story=story, line=line)


class InvalidCommandError(AsyncyError):

    def __init__(self, name, story=None, line=None):
        message = None
        if name is not None:
            message = name + ' is not implemented'

        super().__init__(message, story=story, line=line)


class K8sError(AsyncyError):

    def __init__(self, story=None, line=None, message=None):
        super().__init__(message, story=story, line=line)


class ServiceNotFound(AsyncyError):

    def __init__(self, story=None, line=None, name=None):
        assert name is not None
        super().__init__(
            f'The service "{name}" was not found in the Asyncy Hub. '
            f'Hint: 1. Check with the Asyncy team if this service has '
            f'been made public; 2. Service names are case sensitive',
            story=story, line=line)


class ActionNotFound(AsyncyError):

    def __init__(self, story=None, line=None, service=None, action=None):
        super().__init__(
            f'The action "{action}" was not found in the service "{service}". '
            f'Hint: Check the Asyncy Hub for a list of supported '
            f'actions for this service.',
            story=story, line=line)


class OmgPropertyValueMismatchError(AsyncyError):
    """
    Raised when value does not match type.
    """
    def __init__(self, value, type):
        super().__init__(
            f'The property value {value}'
            f'should be of type {type}.'
            f'It does not adhere to the microservice '
            f'service contract.')
        self.value = value
        self.type = type

    def __str__(self):
        return(str(self.value))


class OmgPropertyTypeMissingError(AsyncyError):
    """
    Raised when value does not match type.
    """
    def __init__(self, value, type):
        super().__init__(
            f'The property value {value} '
            f'does not have a type {type} specifed.'
            f'Please check microservice.yml '
            f'and specify type for each value')
        self.value = value
        self.type = type

    def __str__(self):
        return(str(self.value))


class EnvironmentVariableNotFound(AsyncyError):
    def __init__(self, service=None, variable=None, story=None, line=None):
        assert service is not None
        assert variable is not None
        super().__init__(
            f'The service "{service}" requires an environment variable '
            f'"{variable}" which was not specified. '
            f'Please set it by running '
            f'"$ asyncy config set {service}.{variable}=<value>" '
            f'in your Asyncy app directory', story, line)
