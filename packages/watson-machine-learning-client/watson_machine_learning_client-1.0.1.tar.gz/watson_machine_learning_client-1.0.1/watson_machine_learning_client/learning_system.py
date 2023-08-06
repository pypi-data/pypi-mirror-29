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
from watson_machine_learning_client.utils import get_headers, STR_TYPE, get_url, docstring_parameter, STR_TYPE_NAME, print_text_header_h2, print_text_header_h1, str_type_conv, meta_props_str_conv
from watson_machine_learning_client.metanames import LearningSystemMetaNames
import base64
from watson_machine_learning_client.wml_resource import WMLResource
from multiprocessing import Pool
from watson_machine_learning_client.wml_client_error import MissingValue, WMLClientError


class LearningSystem(WMLResource):
    """
       Continuous Learning System.
    """

    def __init__(self, client, wml_credentials, wml_token, instance_details):
        WMLResource.__init__(self, __name__, client, wml_credentials, wml_token, instance_details)
        self._base_published_models_url = wml_credentials[u'url'] + '/v3/wml_instances/' + wml_credentials[u'instance_id'] + '/published_models'
        self.ConfigurationMetaNames = LearningSystemMetaNames()
        self._run_uid_to_model_uid_mapping = {}

    def _get_model_uid_by_run_uid(self, run_uid):

        if run_uid not in self._run_uid_to_model_uid_mapping:
            models = self._client.repository.get_model_details()

            pool = Pool(processes=4)

            def url(model_uid):
                return self._base_published_models_url + '/' + model_uid + '/learning_iterations'

            headers = get_headers(self._wml_token)

            tasks = [pool.apply_async(get_url, (url(resource[u'metadata'][u'guid']), headers)) for resource in models[u'resources']]

            for task in tasks:
                response = task.get()
                result = self._handle_response(200, u'getting learning iterations', response, True)

                for resource in result[u'resources']:
                    self._run_uid_to_model_uid_mapping.update({resource[u'metadata'][u'guid']: resource[u'entity'][u'published_model'][u'guid']})

            pool.close()

        return self._run_uid_to_model_uid_mapping[run_uid]

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def setup(self, model_uid, meta_props):
        """
            Setup continuous learning system for stored model.

            :param model_uid: ID of stored model
            :type model_uid: {str_type}
            :param meta_props: learning system configuration meta data
            :type meta_props: dict

            :return: learning system configuration details
            :rtype: dict

            A way you might use me is

            >>> learning_system = client.learning_system.create(model_uid, meta_props=configuration)
        """
        model_uid = str_type_conv(model_uid)
        self._validate_type(model_uid, u'model_uid', STR_TYPE, True)
        self._validate_type(meta_props, u'meta_props', dict, True)
        meta_props_str_conv(meta_props)
        self.ConfigurationMetaNames._validate(meta_props)

        spark_instance = {
            u'credentials': meta_props[self.ConfigurationMetaNames.SPARK_REFERENCE],
            u'version': u'2.0'
        }

        headers = {
            u'Content-Type': u'application/json',
            u'Authorization': u'Bearer ' + self._wml_token,
            u'X-Spark-Service-Instance': base64.b64encode(json.dumps(spark_instance).encode('utf-8'))
        }

        payload = {
            u'feedback_data_reference': meta_props[self.ConfigurationMetaNames.FEEDBACK_DATA_REFERENCE],
            u'min_feedback_data_size': meta_props[self.ConfigurationMetaNames.MIN_FEEDBACK_DATA_SIZE],
            u'auto_retrain': meta_props[self.ConfigurationMetaNames.AUTO_RETRAIN],
            u'auto_redeploy': meta_props[self.ConfigurationMetaNames.AUTO_REDEPLOY]
        }

        response = requests.put(
            self._base_published_models_url + u'/' + model_uid + u'/learning_configuration',
            json=payload,
            headers=headers
        )

        return self._handle_response(200, u'creating learning system', response, True)

    def update(self, model_uid, changes):
        """
        Updates existing learning system metadata.

        :param model_uid: UID of model which learning system should be updated
        :type model_uid: str

        :param changes: elements which should be changed, where keys are LearningSystemMetaNames
        :type changes: dict

        :return: metadata of updated learning system
        :rtype: dict
        """
        model_uid = str_type_conv(model_uid)
        self._validate_type(model_uid, u'model_uid', STR_TYPE, True)
        self._validate_type(changes, u'changes', dict, True)
        meta_props_str_conv(changes)
        WMLResource._validate_meta_prop(changes, self.ConfigurationMetaNames.FEEDBACK_DATA_REFERENCE, dict, False)
        WMLResource._validate_meta_prop(changes, self.ConfigurationMetaNames.SPARK_REFERENCE, dict, False)
        WMLResource._validate_meta_prop(changes, self.ConfigurationMetaNames.MIN_FEEDBACK_DATA_SIZE, int, False)
        WMLResource._validate_meta_prop(changes, self.ConfigurationMetaNames.AUTO_RETRAIN, STR_TYPE, False)
        WMLResource._validate_meta_prop(changes, self.ConfigurationMetaNames.AUTO_REDEPLOY, STR_TYPE, False)

        def _decide_op(details, path):
            try:
                if len(path) == 1:
                    x = details[path[0]]
                    if x is not None:
                        return u'replace'
                    else:
                        return u'add'
                else:
                    return _decide_op(details[path[0]], path[1:])
            except:
                return u'add'

        def _update_patch_payload(patch_payload, details, changes, path, meta_name, value=None):
            if meta_name in changes:
                if value is None:
                    value = changes[meta_name]

                patch_payload.append(
                    {
                        u'op': _decide_op(details, path),
                        u'path': u'/' + u'/'.join(path),
                        u'value': value
                    }
                )

        details = self.get_details(model_uid)

        patch_payload = []
        _update_patch_payload(patch_payload, details, changes, [u'feedback_data_reference'], self.ConfigurationMetaNames.FEEDBACK_DATA_REFERENCE)
        _update_patch_payload(patch_payload, details, changes, [u'min_feedback_data_size'], self.ConfigurationMetaNames.MIN_FEEDBACK_DATA_SIZE)
        _update_patch_payload(patch_payload, details, changes, [u'spark_service', u'credentials'], self.ConfigurationMetaNames.SPARK_REFERENCE)
        _update_patch_payload(patch_payload, details, changes, [u'auto_retrain'], self.ConfigurationMetaNames.AUTO_RETRAIN)
        _update_patch_payload(patch_payload, details, changes, [u'auto_redeploy'], self.ConfigurationMetaNames.AUTO_REDEPLOY)

        url = self._base_published_models_url + '/' + model_uid + '/learning_configuration'
        response = requests.patch(url, json=patch_payload, headers=get_headers(self._wml_token))
        updated_details = self._handle_response(200, u'learning system patch', response)

        return updated_details

    def get_details(self, model_uid):
        """
            Get details of learning system.

            :param model_uid: ID of model for this learning system
            :type model_uid: str

            A way you might use me is

            >>> learning_system_details = client.learning_system.get_details(model_uid)
        """
        model_uid = str_type_conv(model_uid)
        self._validate_type(model_uid, u'model_uid', STR_TYPE, True)

        response = requests.get(
            self._base_published_models_url + u'/' + model_uid,
            headers=get_headers(self._wml_token)
        )

        details = self._handle_response(200, u'getting learning system details', response, True)

        return details[u'entity'][u'learning_configuration']

    def list(self):
        """
            List existing learning systems.

            A way you might use me is

            >>> client.learning_system.list()
        """
        from tabulate import tabulate

        models = self._client.repository.get_model_details()[u'resources']
        models = [x for x in models if 'learning_configuration' in x[u'entity']]

        values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'entity'][u'model_type'], m[u'entity'][u'learning_configuration'][u'auto_retrain'], m[u'entity'][u'learning_configuration'][u'auto_redeploy'], m[u'entity'][u'learning_configuration'][u'min_feedback_data_size']) for m in models]

        print(tabulate([['MODEL GUID', 'MODEL NAME', 'FRAMEWORK', 'RETRAIN', 'REDEPLOY', 'MIN FEEDBACK ROWS']] + values))

    def run(self, model_uid, asynchronous=True):
        """
            Run learning iterations.

            :param model_uid: ID of stored model
            :type model_uid: str

            :param asynchronous: if the run should be asynchronous (optional)
            :type asynchronous: bool

            A way you might use me is

            >>> client.learning_system.run(model_uid)
            >>> client.learning_system.run(model_uid, asynchronous=False)
        """
        model_uid = str_type_conv(model_uid)
        self._validate_type(model_uid, u'model_uid', STR_TYPE, True)
        self._validate_type(asynchronous, u'asynchronous', bool, True)

        response = requests.post(
            self._base_published_models_url + '/' + model_uid + '/learning_iterations',
            json={},
            headers=get_headers(self._wml_token)
        )

        self._handle_response(201, u'running learning iterations', response, False)

        result = requests.get(
            response.headers[u'Location'],
            headers=get_headers(self._wml_token)
        )

        details = self._handle_response(200, u'getting learning iterations details', result, True)

        if asynchronous:
            return details
        else:
            run_uid = self.get_run_uid(details)

            import time
            print_text_header_h1(u'Synchronous run for uid: \'{}\' started'.format(run_uid))

            status = details[u'entity'][u'status'][u'state']
            print(status, end='')
            last_status = status

            while True:
                time.sleep(5)
                details = self.get_run_details(run_uid)
                status = details[u'entity'][u'status'][u'state']
                if status == last_status:
                    print(u'.', end='')
                else:
                    print(u'\n' + status, end='')
                    last_status = status

                if status != u'INITIALIZED' and status != u'RUNNING':
                    break

            if status == u'COMPLETED':
                print(u'')
                print_text_header_h2(
                    u'Successfully finished learning iteration run, run_uid=\'{}\''.format(run_uid))
                return details
            else:
                print_text_header_h2(u'Run failed')
                try:  # TODO better handling
                    for error in details[u'entity'][u'status'][u'failure'][u'errors']:
                        print(error[u'message'])

                    raise WMLClientError(
                        u'Run failed. Errors: ' + str(
                            details[u'entity'][u'status'][u'failure'][
                                u'errors']))
                except Exception as e:
                    self._logger.debug("Run failed: " + str(e))
                    raise WMLClientError(u'Run failed.')

    def get_run_uid(self, run_details):
        """
            Get uid of run (learning iteration).

            :param run_details: details of run
            :type run_details: dict

            :return: run uid
            :rtype: str

            A way you might use me is

            >>> run_uid = client.learning_system.get_run_uid(run_details)
        """
        self._validate_type(run_details, u'run_details', dict, True)

        try:
            uid = run_details.get(u'metadata').get(u'guid')
        except Exception as e:
            raise WMLClientError(u'Getting run uid from run details failed.', e)

        if uid is None:
            raise MissingValue(u'run_details.metadata.guid')

        return uid

    def get_run_href(self, run_details):
        """
            Get href of run (learning iteration).

            :param run_details: details of run
            :type run_details: dict

            :return: run href
            :rtype: str

            A way you might use me is

            >>> run_uid = client.learning_system.get_run_href(run_details)
        """
        self._validate_type(run_details, u'run_details', dict, True)

        try:
            uid = run_details.get(u'metadata').get(u'url')
        except Exception as e:
            raise WMLClientError(u'Getting run href from run details failed.', e)

        if uid is None:
            raise MissingValue(u'run_details.metadata.url')

        return uid

    def get_runs(self, model_uid):
        """
            Get learning iterations (runs).

            :param model_uid: ID of stored model
            :type model_uid: str

            A way you might use me is

            >>> runs_details = client.learning_system.get_runs(model_uid)
        """
        model_uid = str_type_conv(model_uid)
        self._validate_type(model_uid, u'model_uid', STR_TYPE, True)

        response = requests.get(
            self._base_published_models_url + '/' + model_uid + '/learning_iterations',
            headers=get_headers(self._wml_token)
        )

        details = self._handle_response(200, u'getting learning iterations', response, True)

        for resource in details[u'resources']:
            self._run_uid_to_model_uid_mapping.update({resource[u'metadata'][u'guid']: model_uid})

        return details

    def get_metrics(self, model_uid):
        """
            Get evaluation metrics.

            :param model_uid: ID of stored model
            :type model_uid: str

            A way you might use me is

            >>> runs_details = client.learning_system.get_metrics(model_uid)
        """
        model_uid = str_type_conv(model_uid)
        self._validate_type(model_uid, u'model_uid', STR_TYPE, True)

        response = requests.get(
            self._base_published_models_url + '/' + model_uid + '/evaluation_metrics',
            headers=get_headers(self._wml_token)
        )

        return self._handle_response(200, u'getting evaluation metrics', response, True)

    def list_metrics(self, model_uid):
        """
            Get evaluation metrics.

            :param model_uid: ID of stored model
            :type model_uid: str

            A way you might use me is

            >>> runs_details = client.learning_system.get_metrics(model_uid)
        """
        model_uid = str_type_conv(model_uid)
        self._validate_type(model_uid, u'model_uid', STR_TYPE, True)

        from tabulate import tabulate

        metrics = self.get_metrics(model_uid)[u'resources']

        def metric_names(m):
            return '\n'.join([x[u'name'] for x in m[u'values']])

        def metric_values(m):
            return '\n'.join([str(x[u'value']) for x in m[u'values']])

        def metric_thresholds(m):
            return '\n'.join([str(x[u'threshold']) for x in m[u'values']])

        values = [(m[u'phase'], m[u'timestamp'], metric_names(m), metric_values(m), metric_thresholds(m), m[u'model_version_url'][-36:-1]) for m in metrics]

        print(tabulate([['PHASE', 'TIMESTAMP', 'METRIC NAME', 'METRIC VALUE', 'METRIC THRESH.', 'VERSION']] + values))

    def list_runs(self, model_uid=None):
        """
           List learning iterations.

           :param model_uid: ID of stored model (optional)
           :type model_uid: str

           A way you might use me is

           >>> client.repository.list_runs()
        """
        model_uid = str_type_conv(model_uid)
        self._validate_type(model_uid, u'model_uid', STR_TYPE, False)

        from tabulate import tabulate

        if model_uid is None:
            details = self._client.repository.get_model_details()
            model_resources = details[u'resources']
            pool = Pool(processes=4)

            def url(model_uid):
                return self._base_published_models_url + '/' + model_uid + '/learning_iterations'
            headers = get_headers(self._wml_token)

            models_runs = [pool.apply_async(get_url, (url(resource[u'metadata'][u'guid']), headers)) for resource in
                            model_resources]

            result = []
            for model_runs in models_runs:
                try:
                    response = model_runs.get()
                    response_text = self._handle_response(200, u'getting learning iterations', response)
                    result.extend(response_text[u'resources'])
                    for resource in response_text[u'resources']:
                        self._run_uid_to_model_uid_mapping.update({resource[u'metadata'][u'guid']: resource[u'entity'][u'published_model'][u'guid']})
                except Exception as e:
                    self._logger.error(e)

            pool.close()

            result = sorted(result, key=lambda x: x[u'metadata'][u'created_at'])

            run_values = [
                (m[u'metadata'][u'guid'], m[u'metadata'][u'created_at'], m[u'entity'][u'status'][u'state'], m[u'entity'][u'published_model'][u'guid'])
                for m in result]
            table = tabulate([[u'RUN GUID', u'CREATED', u'STATE', u'MODEL GUID']] + run_values)
            print(table)

        else:
            run_resources = self.get_runs(model_uid)[u'resources']
            run_values = [
                (m[u'metadata'][u'guid'], m[u'metadata'][u'created_at'], m[u'entity'][u'status'][u'state'])
                for m in run_resources]
            table = tabulate([[u'RUN GUID', u'CREATED', u'STATE']] + run_values)
            print(table)

    def get_run_details(self, run_uid):
        """
            Get run details.

            :param run_uid: ID of learning iteration run
            :type run_uid: str

            A way you might use me is

            >>> run_details = client.learning_system.get_run_details(run_uid)
        """
        run_uid = str_type_conv(run_uid)
        self._validate_type(run_uid, u'run_uid', STR_TYPE, True)

        model_uid = self._get_model_uid_by_run_uid(run_uid)

        response = requests.get(
            self._base_published_models_url + '/' + model_uid + '/learning_iterations/' + run_uid,
            headers=get_headers(self._wml_token)
        )

        return self._handle_response(200, u'getting learning iteration details', response, True)

    def send_feedback(self, model_uid, feedback_data, fields=None):
        """
            Send feedback data to learning system.

            :param model_uid: ID of model
            :type model_uid: str
            :param feedback_data: rows of feedback data to be send
            :type feedback_data: list
            :param fields: list of fields (optional)
            :type fields: list

            A way you might use me is

            >>> client.learning_system.send_feedback(model_uid, [["a1", 1, 1.0], ["a2", 2, 3.4]])
            >>> client.learning_system.send_feedback(model_uid, [["a1", 1.0], ["a2", 3.4]], fields=["id", "value"])
        """
        model_uid = str_type_conv(model_uid)
        self._validate_type(model_uid, "model_uid", str, True)
        self._validate_type(feedback_data, "feedback_data", list, True)
        self._validate_type(fields, "fields", list, False)

        data = {
            "values": feedback_data
        }

        if fields is not None:
            data.update({"fields": fields})

        response = requests.post(
            self._base_published_models_url + '/' + model_uid + '/feedback',
            json=data,
            headers=get_headers(self._wml_token)
        )

        return self._handle_response(200, u'send feedback', response, True)
