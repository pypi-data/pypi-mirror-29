################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
import requests
import json
from watson_machine_learning_client.utils import get_headers, DEPLOYMENT_DETAILS_TYPE, print_text_header_h1, print_text_header_h2, STR_TYPE, STR_TYPE_NAME, docstring_parameter, str_type_conv
from watson_machine_learning_client.wml_client_error import WMLClientError, MissingValue, ApiRequestFailure
from watson_machine_learning_client.href_definitions import is_uid
from watson_machine_learning_client.wml_resource import WMLResource


class Deployments(WMLResource):
    """
        Deploy and score published models.
    """
    def __init__(self, client, wml_credentials, wml_token, instance_details):
        WMLResource.__init__(self, __name__, client, wml_credentials, wml_token, instance_details)

    def _get_url_for_uid(self, deployment_uid):
        response_get = requests.get(
            self._href_definitions.get_deployments_href(),
            headers=get_headers(self._wml_token))

        try:
            if response_get.status_code == 200:
                for el in json.loads(response_get.text).get(u'resources'):
                    if el.get(u'metadata').get(u'guid') == deployment_uid:
                        return el.get(u'metadata').get('url')
            else:
                raise ApiRequestFailure(u'Couldn\'t generate url from uid: \'{}\'.'.format(deployment_uid), response_get)
        except Exception as e:
            raise WMLClientError(u'Failed during getting url for uid: \'{}\'.'.format(deployment_uid), e)

        raise WMLClientError(u'No matching url for uid: \'{}\'.'.format(deployment_uid))

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_details(self, deployment_uid=None):
        """
           Get information about your deployment(s).

           :param deployment_uid:  Deployment UID (optional)
           :type deployment_uid: {str_type}

           :returns: metadata of deployment(s)
           :rtype: dict

           A way you might use me is:

            >>> deployment_details = client.deployments.get_details(deployment_uid)
            >>> deployment_details = client.deployments.get_details(deployment_uid=deployment_uid)
            >>> deployments_details = client.deployments.get_details()
        """
        deployment_uid = str_type_conv(deployment_uid)
        Deployments._validate_type(deployment_uid, u'deployment_uid', STR_TYPE, False)

        if deployment_uid is not None and not is_uid(deployment_uid):
            raise WMLClientError(u'\'deployment_uid\' is not an uid: \'{}\''.format(deployment_uid))

        if deployment_uid is not None:
            deployment_url = self._get_url_for_uid(deployment_uid)
        else:
            deployment_url = self._instance_details.get(u'entity').get(u'deployments').get(u'url')

        response_get = requests.get(
            deployment_url,
            headers=get_headers(self._wml_token))

        return self._handle_response(200, u'getting deployment(s) details', response_get)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_status(self, deployment_uid):
        """
            Get status of deployment creation.

            :param deployment_uid: Guid of deployment
            :type deployment_uid: {str_type}

            :returns: status of deployment creation
            :rtype: {str_type}

            A way you might use me is:

             >>> status = client.deployments.get_status(deployment_uid)
        """
        deployment_uid = str_type_conv(deployment_uid)
        Deployments._validate_type(deployment_uid, u'deployment_uid', STR_TYPE, True)

        details = self.get_details(deployment_uid)
        return self._get_required_element_from_dict(details, u'deployment_details', [u'entity', u'status'])

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def create(self, model_uid, name, description=u'Model deployment', asynchronous=False):
        """
            Create model deployment (online).

            :param model_uid:  Published model UID
            :type model_uid: {str_type}
            :param name: Deployment name
            :type name: {str_type}
            :param description: Deployment description
            :type description: {str_type}
            :param asynchronous: if `False` then will wait until deployment will be fully created before returning
            :type asynchronous: bool

            :returns: details of created deployment
            :rtype: dict

            A way you might use me is:

             >>> deployment = client.deployments.create(model_uid, 'Deployment X', 'Online deployment of XYZ model.')
         """
        model_uid = str_type_conv(model_uid)
        Deployments._validate_type(model_uid, u'model_uid', STR_TYPE, True)
        name = str_type_conv(name)
        Deployments._validate_type(name, u'name', STR_TYPE, True)
        description = str_type_conv(description)
        Deployments._validate_type(description, u'description', STR_TYPE, True)

        url = self._instance_details.get(u'entity').get(u'published_models').get(u'url') + u'/' + model_uid + u'/' + u'deployments?sync=false'
        response_online = requests.post(
            url,
            json={u'name': name, u'description': description, u'type': u'online'},
            headers=get_headers(self._wml_token))

        if asynchronous:
            if response_online.status_code == 202:
                deployment_details = json.loads(response_online.text)
                deployment_uid = self.get_uid(deployment_details)
                print_text_header_h1(u'Asynchronous deployment creation for uid: \'{}\' started'.format(deployment_uid))
                print(u'To monitor status of your deployment use: client.deployments.get_status(\"{}\")'.format(deployment_uid))
                print(u'Scoring url for this deployment: \"{}\"'.format(self.get_scoring_url(deployment_details)))
                return deployment_details
            else:
                return self._handle_response(201, u'deployment creation', response_online)
        else:
            if response_online.status_code == 202:
                deployment_details = json.loads(response_online.text)
                deployment_uid = self.get_uid(deployment_details)

                import time
                print_text_header_h1(u'Synchronous deployment creation for uid: \'{}\' started'.format(deployment_uid))

                status = deployment_details[u'entity'][u'status']
                print(status, end='')
                last_status = status

                while True:
                    time.sleep(5)
                    deployment_details = self._client.deployments.get_details(deployment_uid)
                    status = deployment_details[u'entity'][u'status']
                    if status == last_status:
                        print(u'.', end='')
                    else:
                        print(u'\n' + status, end='')
                    last_status = status

                    if status != u'DEPLOY_IN_PROGRESS':
                        break

                if status == u'DEPLOY_SUCCESS':
                    print(u'')
                    print_text_header_h2(u'Successfully finished deployment creation, deployment_uid=\'{}\''.format(deployment_uid))
                    return deployment_details
                else:
                    print_text_header_h2(u'Deployment creation failed')
                    try:  # TODO better handling
                        for error in deployment_details[u'entity'][u'status_details'][u'failure'][u'errors']:
                            error_obj = json.loads(error)
                            print(error_obj[u'message'])

                        raise WMLClientError(
                            u'Deployment creation failed. Errors: ' + str(deployment_details[u'entity'][u'status_details'][u'failure'][
                                u'errors']))
                    except:
                        raise WMLClientError(u'Deployment creation failed.')
            elif response_online.status_code == 201:
                deployment_details = json.loads(response_online.text)
                deployment_uid = self.get_uid(deployment_details)
                print_text_header_h1(u'Synchronous deployment creation for uid: \'{}\' started'.format(deployment_uid))
                print(u'DEPLOY_SUCCESS')
                print_text_header_h2(u'Successfully finished deployment creation, deployment_uid=\'{}\''.format(deployment_uid))
                return deployment_details
            else:
                error_msg = u'Deployment creation failed'
                reason = response_online.text
                print(reason)
                print_text_header_h2(error_msg)
                raise WMLClientError(error_msg + u'. Error: ' + reason)

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_scoring_url(deployment):
        """
            Get scoring_url from deployment details.

            :param deployment: Created deployment details
            :type deployment: dict

            :returns: scoring endpoint URL that is used for making scoring requests
            :rtype: {str_type}

            A way you might use me is:

             >>> scoring_url = client.deployments.get_scoring_url(deployment)
        """
        Deployments._validate_type(deployment, u'deployment', dict, True)
        Deployments._validate_type_of_details(deployment, DEPLOYMENT_DETAILS_TYPE)

        try:
            url = deployment.get(u'entity').get(u'scoring_url')
        except Exception as e:
            raise WMLClientError(u'Getting scoring url for deployment failed.', e)

        if url is None:
            raise MissingValue(u'entity.scoring_url')

        return url

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_uid(deployment_details):
        """
            Get deployment_uid from deployment details.

            :param deployment_details: Created deployment details
            :type deployment_details: dict

            :returns: deployment UID that is used to manage the deployment
            :rtype: {str_type}

            A way you might use me is:

            >>> deployment_uid = client.deployments.get_uid(deployment)
        """
        Deployments._validate_type(deployment_details, u'deployment_details', dict, True)
        Deployments._validate_type_of_details(deployment_details, DEPLOYMENT_DETAILS_TYPE)

        try:
            uid = deployment_details.get(u'metadata').get(u'guid')
        except Exception as e:
            raise WMLClientError(u'Getting deployment uid from deployment details failed.', e)

        if uid is None:
            raise MissingValue(u'deployment_details.metadata.guid')

        return uid

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_url(deployment_details):
        """
            Get deployment_url from deployment details.

            :param deployment_details:  Created deployment details
            :type deployment_details: dict

            :returns: deployment URL that is used to manage the deployment
            :rtype: {str_type}

            A way you might use me is:

            >>> deployment_url = client.deployments.get_url(deployment)
        """
        Deployments._validate_type(deployment_details, u'deployment_details', dict, True)
        Deployments._validate_type_of_details(deployment_details, DEPLOYMENT_DETAILS_TYPE)

        try:
            url = deployment_details.get(u'metadata').get(u'url')
        except Exception as e:
            raise WMLClientError(u'Getting deployment url from deployment details failed.', e)

        if url is None:
            raise MissingValue(u'deployment_details.metadata.url')

        return url

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete(self, deployment_uid):
        """
            Delete model deployment.

            :param deployment_uid: Deployment UID
            :type deployment_uid: {str_type}

            A way you might use me is:

            >>> client.deployments.delete(deployment_uid)
        """
        deployment_uid = str_type_conv(deployment_uid)
        Deployments._validate_type(deployment_uid, u'deployment_uid', STR_TYPE, True)

        if deployment_uid is not None and not is_uid(deployment_uid):
            raise WMLClientError(u'\'deployment_uid\' is not an uid: \'{}\''.format(deployment_uid))

        deployment_url = self._get_url_for_uid(deployment_uid)

        response_delete = requests.delete(
            deployment_url,
            headers=get_headers(self._wml_token))

        self._handle_response(204, u'deployment deletion', response_delete, False)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def score(self, scoring_url, payload):
        """
            Make scoring requests against deployed model.

            :param scoring_url:  scoring endpoint URL
            :type scoring_url: {str_type}
            :param payload: records to score
            :type payload: dict

            :returns: scoring result containing prediction and probability
            :rtype: dict

            A way you might use me is:

            >>> scoring_payload = {'fields': ['GENDER','AGE','MARITAL_STATUS','PROFESSION'], 'values': [['M',23,'Single','Student'],['M',55,'Single','Executive']]}
            >>> predictions = client.deployments.score(scoring_url, scoring_payload)
        """
        scoring_url = str_type_conv(scoring_url)
        Deployments._validate_type(scoring_url, u'scoring_url', STR_TYPE, True)
        Deployments._validate_type(payload, u'payload', dict, True)

        response_scoring = requests.post(
            scoring_url,
            json=payload,
            headers=get_headers(self._wml_token))

        return self._handle_response(200, u'scoring', response_scoring)

    def list(self):
        """
           List deployments.

           A way you might use me is:

           >>> client.deployments.list()
        """
        from tabulate import tabulate

        details = self.get_details()
        resources = details[u'resources']
        values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'entity'][u'type'], m[u'entity'][u'status'], m[u'metadata'][u'created_at'], m[u'entity'][u'model_type']) for m in resources]
        table = tabulate([[u'GUID', u'NAME', u'TYPE', u'STATE', u'CREATED', u'FRAMEWORK']] + values)
        print(table)

    def get_uids(self):
        """
            Get all deployments uids.

            :returns: list of uids
            :rtype: list

            A way you might use me is:

            >>> deployments_uids = client.deployments.get_uids()
        """
        details = self.get_details()
        resources = details[u'resources']
        uids = []

        for x in resources:
            uids.append(x['metadata']['guid'])

        return uids
