################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

import json
from watson_machine_learning_client.wml_client_error import MissingValue, WMLClientError, NoWMLCredentialsProvided, ApiRequestFailure, UnexpectedType, MissingMetaProp
from watson_machine_learning_client.href_definitions import HrefDefinitions
from watson_machine_learning_client.log_util import get_logger
from watson_machine_learning_client.utils import get_type_of_details, INSTANCE_DETAILS_TYPE, STR_TYPE, str_type_conv

class WMLResource:
    def __init__(self, name, client, wml_credentials, wml_token, instance_details):
        self._logger = get_logger(name)
        WMLResource._validate_type(client, u'client', object, True)
        if wml_credentials is None:
            raise NoWMLCredentialsProvided
        WMLResource._validate_type(wml_credentials, u'wml_credentials', dict, True)
        wml_token = str_type_conv(wml_token)
        WMLResource._validate_type(wml_token, u'wml_token', STR_TYPE, True)
        WMLResource._validate_type(instance_details, u'instance_details', dict, True)
        WMLResource._validate_type_of_details(instance_details, INSTANCE_DETAILS_TYPE)
        self._client = client
        self._wml_credentials = wml_credentials
        self._wml_token = wml_token
        self._instance_details = instance_details
        self._href_definitions = HrefDefinitions(wml_credentials)

    def _handle_response(self, expected_status_code, operationName, response, json_response=True):
        if response.status_code == expected_status_code:
            self._logger.info(u'Successfully finished {} for url: \'{}\''.format(operationName, response.url))
            self._logger.debug(u'Response({} {}): {}'.format(response.request.method, response.url, response.text))
            if json_response:
                try:
                    return json.loads(response.text)
                except Exception as e:
                    raise WMLClientError(u'Failure during parsing json response: \'{}\''.format(response.text), e)
            else:
                return response.text
        else:
            raise ApiRequestFailure(u'Failure during {}.'.format(operationName), response)

    @staticmethod
    def _get_required_element_from_dict(el, root_path, path):
        WMLResource._validate_type(el, root_path, dict)
        WMLResource._validate_type(root_path, u'root_path', STR_TYPE)
        WMLResource._validate_type(path, u'path', list)

        if path.__len__() < 1:
            raise WMLClientError(u'Unexpected path length: {}'.format(path.__len__))

        try:
            new_el = el[path[0]]
            new_path = path[1:]
        except Exception as e:
            raise MissingValue(root_path + '.' + str(path[0]), e)

        if path.__len__() > 1:
            return WMLResource._get_required_element_from_dict(new_el, root_path + u'.' + path[0], new_path)
        else:
            if new_el is None:
                raise MissingValue(root_path + u'.' + str(path[0]))

            return new_el

    @staticmethod
    def _validate_type(el, el_name, expected_type, mandatory=True):
        if el_name is None:
            raise MissingValue(u'el_name')

        el_name = str_type_conv(el_name)
        if type(el_name) is not STR_TYPE:
            raise UnexpectedType(u'el_name', STR_TYPE, type(el_name))

        if expected_type is None:
            raise MissingValue(u'expected_type')

        if type(expected_type) is not type and type(expected_type) is not list:
            raise UnexpectedType('expected_type', 'type or list', type(expected_type))

        if type(mandatory) is not bool:
            raise UnexpectedType(u'mandatory', bool, type(mandatory))

        if mandatory and el is None:
            raise MissingValue(el_name)
        elif el is None:
            return

        if type(expected_type) is list:
            try:
                next((x for x in expected_type if isinstance(el, x)))
                return True
            except StopIteration:
                return False
        else:
            if not isinstance(el, expected_type):
                raise UnexpectedType(el_name, expected_type, type(el))

    @staticmethod
    def _validate_meta_prop(meta_props, name, expected_type, mandatory=True):
        if name in meta_props:
            WMLResource._validate_type(meta_props[name], u'meta_props.' + name, expected_type, mandatory)
        else:
            if mandatory:
                raise MissingMetaProp(name)

    @staticmethod
    def _validate_type_of_details(details, expected_type):
        actual_type = get_type_of_details(details)
        if actual_type != expected_type:
            logger = get_logger(u'_validate_type_of_details')
            logger.debug(u'Unexpected type of \'{}\', expected: \'{}\', actual: \'{}\', occured for details: {}'.format(u'details', expected_type, actual_type, details))
            raise UnexpectedType(u'details', expected_type, actual_type)
