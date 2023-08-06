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
import re
import tqdm
from watson_machine_learning_client.utils import get_headers
import time
from watson_machine_learning_client.wml_client_error import MissingValue, WMLClientError
from watson_machine_learning_client.href_definitions import is_uid
from watson_machine_learning_client.wml_resource import WMLResource
from multiprocessing import Pool
from watson_machine_learning_client.utils import print_text_header_h1, print_text_header_h2, EXPERIMENT_RUN_DETAILS_TYPE, format_metrics, STR_TYPE, STR_TYPE_NAME, docstring_parameter, group_metrics, str_type_conv
from watson_machine_learning_client.hpo import HPOParameter, HPOMethodParam


def _get_details_helper(url, headers, setting=None):
    from watson_machine_learning_client.log_util import get_logger
    logger = get_logger(u'experiments._get_details_helper')
    response_get = requests.get(
        url + u'/runs',
        headers=headers)
    if response_get.status_code == 200:
        logger.debug(u'Successfully got runs details ({}): {}'.format(response_get.status_code, response_get.text))
        details = json.loads(response_get.text)

        if u'resources' in details:
            resources = details[u'resources']
        else:
            resources = [details]

        if setting is not None:
            for r in resources:
                r[u'entity'].update({u'_parent_settings': setting})
        return resources
    else:
        logger.warning(u'Failure during getting runs details ({}): {}'.format(response_get.status_code, response_get.text))
        return []


class Experiments(WMLResource):
    """
       Run new experiment.
    """

    @staticmethod
    def HPOParameter(name, values=None, max=None, min=None, step=None):
        return HPOParameter(name, values, max, min, step)

    @staticmethod
    def HPOMethodParam(name=None, value=None):
        return HPOMethodParam(name, value)

    def __init__(self, client, wml_credentials, wml_token, instance_details):
        WMLResource.__init__(self, __name__, client, wml_credentials, wml_token, instance_details)
        self._base_models_url = wml_credentials['url'] + "/v3/models"
        self._experiments_uids_cache = {}

    def _get_experiment_uid(self, experiment_run_uid=None, experiment_run_url=None):
        if experiment_run_uid is None and experiment_run_url is None:
            raise MissingValue(u'experiment_run_id/experiment_run_url')

        if experiment_run_uid is not None and experiment_run_uid in self._experiments_uids_cache:
            return self._experiments_uids_cache[experiment_run_uid]

        if experiment_run_url is not None:
            m = re.search(u'.+/v3/experiments/{[^\/]+}/runs/{[^\/]+}', experiment_run_url)
            _experiment_id = m.group(1)
            _experiment_run_id = m.group(2)
            self._experiments_uids_cache.update({_experiment_run_id: _experiment_id})
            return _experiment_id

        details = self.get_details()

        resources = details[u'resources']

        try:
            el = [x for x in resources if x[u'metadata'][u'guid'] == experiment_run_uid][0]
        except Exception as e:
            raise WMLClientError(u'Cannot find experiment_uid for experiment_run_uid: \'{}\''.format(experiment_run_uid), e)

        experiment_uid = el[u'experiment'][u'guid']
        self._experiments_uids_cache.update({experiment_run_uid: experiment_uid})
        return experiment_uid

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def run(self, experiment_uid, asynchronous=True):
        """
            Run experiment.

            :param experiment_uid: ID of stored experiment
            :type experiment_uid: {str_type}
            :param asynchronous: Default `True` means that experiment is started and progress can be checked later. `False` - method will wait till experiment end and print experiment stats.
            :type asynchronous: bool

            :return: experiment run details
            :rtype: dict

            A way you might use me is

            >>> experiment_run_status = client.experiments.run(experiment_uid)
            >>> experiment_run_status = client.experiments.run(experiment_uid, asynchronous=False)
        """
        experiment_uid = str_type_conv(experiment_uid)
        Experiments._validate_type(experiment_uid, u'experiment_uid', STR_TYPE, True)
        Experiments._validate_type(asynchronous, u'asynchronous', bool, True)

        run_url = self._href_definitions.get_experiment_runs_href(experiment_uid)

        response = requests.post(run_url, headers=get_headers(self._wml_token))

        # TODO should be 202
        result_details = self._handle_response(200, u'experiment run', response)

        experiment_run_uid = self.get_run_uid(result_details)
        self._experiments_uids_cache.update({experiment_run_uid: experiment_uid})

        if asynchronous:
            return result_details
        else:
            print_text_header_h1(u'Running \'{}\' experiment run'.format(experiment_run_uid))

            status = self.get_status(experiment_run_uid)
            state = status[u'state']
            run_details = self.get_run_details(experiment_run_uid)
            training_uids = self.get_training_uids(run_details)

            pbar = tqdm.tqdm(training_uids)

            for uid in pbar:
                pbar.set_description("Processing %s" % uid)
                train_state = self._client.training.get_status(uid)[u'state']
                state = self.get_status(experiment_run_uid)[u'state']

                if train_state not in ['error', 'completed', 'canceled']:
                    while train_state not in ['error', 'completed', 'canceled']:
                        for i in range(10):
                            time.sleep(1)
                            if i < 5:
                                pbar.set_postfix(training_state=train_state)
                            else:
                                pbar.set_postfix(experiment_state=state)

                        train_state = self._client.training.get_status(uid)['state']
                        pbar.set_postfix(training_state=train_state)
                        state = self.get_status(experiment_run_uid)[u'state']
                        pbar.set_postfix(experiment_state=state)
                else:
                    time.sleep(1)
                    pbar.set_postfix(training_state=train_state)

                pbar.set_postfix(training_state=train_state)

            while state not in ['error', 'completed', 'canceled']:
                state = self.get_status(experiment_run_uid)[u'state']
                pbar.set_postfix(experiment_state=state)

            pbar.close()

            if u'completed' in state:
                print_text_header_h2(u'Run of \'{}\' finished successfully.'.format(str(experiment_run_uid)))
            else:
                print_text_header_h2(
                    u'Run of \'{}\' failed with status: \'{}\'.'.format(experiment_run_uid, str(status)))

            result_details = self.get_run_details(experiment_run_uid)
            self._logger.debug(u'Response({}): {}'.format(state, result_details))
            return result_details

    def get_status(self, experiment_run_uid):
        """
            Get experiment status.

            :param experiment_run_uid: ID of experiment run
            :type experiment_run_uid: bool

            :returns: experiment status
            :rtype: dict

            A way you might use me is

            >>> experiment_status = client.experiments.get_status(experiment_run_uid)
        """
        experiment_run_uid = str_type_conv(experiment_run_uid)
        Experiments._validate_type(experiment_run_uid, u'experiment_run_uid', STR_TYPE, True)
        details = self.get_run_details(experiment_run_uid)

        try:
            status = WMLResource._get_required_element_from_dict(details, u'details', [u'entity', u'experiment_run_status'])
        except Exception as e:
            # TODO more specific
            raise WMLClientError(u'Failed to get from details state of experiment.', e)

        return status

    def get_run_details(self, experiment_run_uid):
        """
           Get metadata of particular experiment run.

           :param experiment_run_uid:  experiment run UID
           :type experiment_run_uid: bool

           :returns: experiment run metadata
           :rtype: dict

           A way you might use me is

           >>> experiment_run_details = client.experiments.get_run_details(experiment_run_uid)
        """
        experiment_run_uid = str_type_conv(experiment_run_uid)
        Experiments._validate_type(experiment_run_uid, u'experiment_run_uid', STR_TYPE, True)

        experiment_uid = self._get_experiment_uid(experiment_run_uid)

        url = self._href_definitions.get_experiment_run_href(experiment_uid, experiment_run_uid)

        response_get = requests.get(
            url,
            headers=get_headers(self._wml_token))
        response = self._handle_response(200, u'getting experiment run details', response_get)
        #setting = self._client.repository.get_experiment_details(experiment_uid)['entity']['settings']
        #response['entity'].update({'_parent_settings': setting})
        return response

    def get_details(self, experiment_uid=None):
        """
           Get metadata of experiment(s) run(s). If no experiment_uid is provided, runs will be listed for all existing experiments.

           :param experiment_uid:  experiment UID (optional)
           :type experiment_uid: bool

           :returns: experiment(s) run(s) metadata
           :rtype: dict

           A way you might use me is

           >>> experiment_details = client.experiments.get_details(experiment_uid)
           >>> experiment_details = client.experiments.get_details()
        """
        experiment_uid = str_type_conv(experiment_uid)
        return self._get_extended_details(experiment_uid, False)

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_run_url(experiment_run_details):
        """
            Get experiment run url.

            :param experiment_run_details: details of experiment run
            :type experiment_run_details: object

            :returns: experiment run url
            :rtype: {str_type}

            A way you might use me is

            >>> experiment_run_url = client.experiments.get_run_url(experiment_run_details)
        """
        Experiments._validate_type(experiment_run_details, u'experiment_run_details', dict, True)
        Experiments._validate_type_of_details(experiment_run_details, EXPERIMENT_RUN_DETAILS_TYPE)

        try:
            url = WMLResource._get_required_element_from_dict(experiment_run_details, u'experiment_run_details', [u'metadata', u'url'])
        except Exception as e:
            raise WMLClientError(u'Failure during getting experiment run url from details.', e)

        # TODO uncomment
        # if not is_url(url):
        #     raise WMLClientError('Experiment url: \'{}\' is invalid.'.format(url))

        return url

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_run_uid(experiment_run_details):
        """
            Get experiment run uid.

            :param experiment_run_details: details of experiment run
            :type experiment_run_details: object

            :returns: experiment run uid
            :rtype: {str_type}

            A way you might use me is

            >>> experiment_run_uid = client.experiments.get_run_uid(experiment_run_details)
        """
        Experiments._validate_type(experiment_run_details, u'experiment_run_details', dict, True)
        Experiments._validate_type_of_details(experiment_run_details, EXPERIMENT_RUN_DETAILS_TYPE)

        try:
            uid = WMLResource._get_required_element_from_dict(experiment_run_details, u'experiment_run_details', [u'metadata', u'guid'])
        except Exception as e:
            raise WMLClientError(u'Failure during getting experiment run uid from details.', e)

        if not is_uid(uid):
            raise WMLClientError(u'Experiment run uid: \'{}\' is invalid.'.format(uid))

        return uid

    @staticmethod
    def get_training_runs(experiment_run_details):
        """
            Get experiment training runs details.

            :param experiment_run_details: details of experiment run
            :type: object

            :returns: training runs
            :rtype: array

            A way you might use me is

            >>> training_runs = client.experiments.get_training_runs(experiment_run_details)
        """
        Experiments._validate_type(experiment_run_details, u'experiment_run_details', dict, True)
        Experiments._validate_type_of_details(experiment_run_details, EXPERIMENT_RUN_DETAILS_TYPE)

        # TODO probably should be just entity.guid
        try:
            training_runs = WMLResource._get_required_element_from_dict(experiment_run_details, u'experiment_run_details',
                                                              [u'entity', u'training_statuses'])
        except Exception as e:
            raise WMLClientError(u'Failure during getting experiment training runs from details.', e)

        if training_runs is None or len(training_runs) <= 0:
            raise MissingValue(u'training_runs')

        return training_runs

    @staticmethod
    def get_training_uids(experiment_run_details):
        """
            Get experiment training uids.

            :param experiment_run_details: details of experiment run
            :type experiment_run_details: object

            :returns: training uids
            :rtype: array

            A way you might use me is

            >>> training_uids = client.experiments.get_training_uids(experiment_run_details)
        """
        Experiments._validate_type(experiment_run_details, u'experiment_run_details', dict, True)
        Experiments._validate_type_of_details(experiment_run_details, EXPERIMENT_RUN_DETAILS_TYPE)

        # TODO probably should be just entity.guid
        try:
            training_uids = [x[u'training_guid'] for x in WMLResource._get_required_element_from_dict(experiment_run_details,
                                                                         u'experiment_run_details',
                                                                        [u'entity', u'training_statuses'])]
        except Exception as e:
            raise WMLClientError(u'Failure during getting experiment training runs from details.', e)

        if training_uids is None or len(training_uids) <= 0:
            raise MissingValue(u'training_uids')

        return training_uids

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete(self, experiment_run_uid):
        """
            Delete experiment run.

            :param experiment_run_uid:  experiment run UID
            :type experiment_run_uid: {str_type}

            A way you might use me is

            >>> client.experiments.delete(experiment_run_uid)
        """
        experiment_run_uid = str_type_conv(experiment_run_uid)
        Experiments._validate_type(experiment_run_uid, u'experiment_run_uid', STR_TYPE, True)

        experiment_uid = self._get_experiment_uid(experiment_run_uid)

        run_url = self._href_definitions.get_experiment_run_href(experiment_uid, experiment_run_uid)

        response = requests.delete(run_url, headers=get_headers(self._wml_token))

        self._handle_response(204, u'experiment deletion', response, False)

    def _get_extended_details(self, experiment_uid=None, extended=True):
        experiment_uid = str_type_conv(experiment_uid)
        Experiments._validate_type(experiment_uid, u'experiment_uid', STR_TYPE, False)

        if experiment_uid is None:
            experiments = self._client.repository.get_experiment_details()

            try:
                urls_and_settings = [(experiment[u'metadata'][u'url'], experiment[u'entity'][u'settings'] if extended else None) for experiment in
                                     experiments[u'resources']]

                self._logger.debug(u'Preparing details for urls and settings: {}'.format(urls_and_settings))

                res = []

                pool = Pool(processes=4)
                tasks = []
                for url_and_setting in urls_and_settings:
                    url = url_and_setting[0]
                    setting = url_and_setting[1]
                    tasks.append(pool.apply_async(_get_details_helper,
                                                  (url, get_headers(self._wml_token), setting)))

                for task in tasks:
                    res.extend(task.get())

                pool.close()

            except Exception as e:
                raise WMLClientError(u'Error during getting all experiments details.', e)
            return {u'resources': res}
        else:
            url = self._href_definitions.get_experiment_runs_href(experiment_uid)

            response_get = requests.get(
                url,
                headers=get_headers(self._wml_token))
            # TODO should be 200
            result = self._handle_response(200, u'getting experiment details', response_get)

            if extended:
                setting = self._client.repository.get_experiment_details(experiment_uid)[u'entity'][u'settings']
                for r in result[u'resources']:
                    r[u'entity'].update({u'_parent_settings': setting})

            return result

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def list_runs(self, experiment_uid=None):
        """
            List experiment runs.

            :param experiment_uid: experiment UID (optional)
            :type experiment_uid: {str_type}

            A way you might use me is

            >>> client.experiments.list_runs()
            >>> client.experiments.list_runs(experiment_uid)
        """
        experiment_uid = str_type_conv(experiment_uid)
        Experiments._validate_type(experiment_uid, u'experiment_uid', STR_TYPE, False)

        from tabulate import tabulate

        details = self._get_extended_details(experiment_uid, True)

        resources = details['resources']

        values = [(m[u'experiment'][u'guid'], m[u'metadata'][u'guid'], m[u'entity'][u'_parent_settings'][u'name'], m[u'entity'][u'experiment_run_status'][u'state'], m[u'metadata'][u'created_at']) for m in resources]
        table = tabulate([[u'GUID (experiment)', u'GUID (run)', u'NAME (experiment)', u'STATE', u'CREATED']] + values)
        print(table)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def list_training_runs(self, experiment_run_uid):
        """
             List training runs triggered by experiment run.

             :param experiment_run_uid: experiment run UID
             :type experiment_run_uid: {str_type}

             A way you might use me is

             >>> client.experiments.list_training_runs(experiment_run_uid)
        """
        experiment_run_uid = str_type_conv(experiment_run_uid)
        Experiments._validate_type(experiment_run_uid, 'experiment_run_uid', STR_TYPE, True)

        from tabulate import tabulate
        details = self._client.experiments.get_run_details(experiment_run_uid)
        training_statuses = details[u'entity'][u'training_statuses']

        values = [(m[u'training_guid'], m[u'training_reference_name'], m[u'state'], m[u'submitted_at'], m[u'finished_at'],
                   format_metrics(self._client.training.get_latest_metrics(m[u'training_guid']))) if u'finished_at' in str(m)
                  else (m[u'training_guid'], m[u'training_reference_name'], m[u'state'], m[u'submitted_at'], u'-',
                        format_metrics(self._client.training.get_latest_metrics(m[u'training_guid']))) for m in training_statuses]

        table = tabulate([[u'GUID (training)', u'NAME', u'STATE', u'SUBMITTED', u'FINISHED', u'PERFORMANCE']] + values)

        print(table)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def monitor_logs(self, experiment_run_uid):
        """
            Monitor experiment run log files (prints log content to console).

            :param experiment_run_uid: ID of experiment run
            :type experiment_run_uid: {str_type}

            A way you might use me is

            >>> client.experiments.monitor_logs(experiment_run_uid)
        """
        experiment_run_uid = str_type_conv(experiment_run_uid)
        Experiments._validate_type(experiment_run_uid, u'experiment_run_uid', STR_TYPE, True)

        try:
            experiment_uid = self.get_run_details(experiment_run_uid)[u'experiment'][u'guid']
        except Exception as e:
            raise WMLClientError(u'Failure during getting experiment uid from experiment run details.', e)

        from lomond import WebSocket
        experiment_monitor_endpoint = self._wml_credentials[u'url'].replace(u'https',
                                                          u'wss') + u'/v3/experiments/' + experiment_uid + u'/runs/' + experiment_run_uid + '/monitor'
        websocket = WebSocket(experiment_monitor_endpoint)
        try:
            websocket.add_header(bytes('Authorization', 'utf-8'), bytes('bearer ' + self._wml_token, 'utf-8'))
        except:
            websocket.add_header(bytes('Authorization'), bytes('bearer ' + self._wml_token))

        print_text_header_h1(u'Monitor started for experiment run: ' + str(experiment_run_uid))

        previous_guid = u''

        for event in websocket:
            if event.name == u'text':
                text = json.loads(event.text)
                if (u'entity' in str(text)) and (u'training_statuses' in str(text)):
                    training_statuses = text[u'entity'][u'training_statuses']
                    for i in training_statuses:
                        if (u'training_guid' in i) and (u'message' in i):
                            msg = i[u'message'].strip()
                            guid = i[u'training_guid'].strip()
                            if msg != '':
                                if guid == previous_guid:
                                    print(msg)
                                else:
                                    if 'training_reference_name' in str(i):
                                        name = i['training_reference_name']
                                        if name != '':
                                            h2_text = guid + " (" + name + ")"
                                        else:
                                            h2_text = guid
                                    else:
                                        h2_text = guid

                                    print_text_header_h2(h2_text)
                                    print(msg)

                                previous_guid = guid

        print_text_header_h2(u'Log monitor done.')

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def monitor_metrics(self, experiment_run_uid):
        """
            Monitor metrics log file (prints metrics to console).

            :param experiment_run_uid: ID of experiment run
            :type run_uid: {str_type}

            A way you might use me is:

            >>> client.experiments.monitor_metrics(experiment_run_uid)
        """
        experiment_run_uid = str_type_conv(experiment_run_uid)

        try:
            experiment_uid = self.get_run_details(experiment_run_uid)[u'experiment'][u'guid']
        except Exception as e:
            raise WMLClientError(u'Failure during getting experiment uid from experiment run details.', e)

        print_text_header_h1(u'Metric monitor started for experiment run: ' + str(experiment_run_uid))

        from lomond import WebSocket
        experiment_monitor_endpoint = self._wml_credentials[u'url'].replace(u'https',
                                                                     u'wss') + u'/v3/experiments/' + experiment_uid + u'/runs/' + experiment_run_uid + '/monitor'
        websocket = WebSocket(experiment_monitor_endpoint)
        try:
            websocket.add_header(bytes('Authorization', 'utf-8'), bytes('bearer ' + self._wml_token, 'utf-8'))
        except:
            websocket.add_header(bytes('Authorization'), bytes('bearer ' + self._wml_token))

        previous_guid = u''

        for event in websocket:
            if event.name == u'text':
                text = json.loads(event.text)
                if (u'entity' in str(text)) and (u'training_statuses' in str(text)):
                    training_statuses = text[u'entity'][u'training_statuses']

                    for i in training_statuses:
                        if u'training_guid' in i:
                            guid = i[u'training_guid'].strip()

                            if u'metrics' in i:
                                metrics = i[u'metrics']
                                if len(metrics) > 0:
                                    metric = metrics[0]
                                    values = u' '.join([x[u'name'] + ':' + str(x[u'value']) for x in metric[u'values']])

                                    metric_msg = u'{} iteration:{} phase:{} {}'.format(metric[u'timestamp'], metric[u'iteration'], metric[u'phase'], values)

                                    if metric_msg != u'':
                                        if guid == previous_guid:
                                            print(metric_msg)
                                        else:
                                            if 'training_reference_name' in str(i):
                                                name = i['training_reference_name']
                                                if name != '':
                                                    h2_text = guid + " (" + name + ")"
                                                else:
                                                    h2_text = guid
                                            else:
                                                h2_text = guid

                                            print_text_header_h2(h2_text)
                                            print(metric_msg)

                                        previous_guid = guid

        print_text_header_h2(u'Metric monitor done.')

    def get_latest_metrics(self, experiment_run_uid):
        """
             Get latest metrics values for experiment run.

             :param experiment_run_uid: ID of training run
             :type experiment_run_uid: str

             :returns: metric values
             :rtype: list

             A way you might use me is:

             >>> client.experiments.get_latest_metrics(experiment_run_uid)
         """
        experiment_run_uid = str_type_conv(experiment_run_uid)
        Experiments._validate_type(experiment_run_uid, 'experiment_run_uid', str, True)

        training_statuses = self.get_run_details(experiment_run_uid)['entity']['training_statuses']

        metrics = []

        for status in training_statuses:
            training_guid_metrics = status['metrics']

            if len(training_guid_metrics) > 0:
                grouped_metrics = group_metrics(training_guid_metrics)

                for key, value in grouped_metrics.items():
                    sorted_value = sorted(value, key=lambda k: k['iteration'])

                metrics.append({"training_guid": status['training_guid'], "training_reference_name": status['training_reference_name'], "metrics": sorted_value[-1]})

        return metrics

    def get_metrics(self, experiment_run_uid):
        """
              Get all metrics values for experiment run.

              :param experiment_run_uid: ID of training run
              :type experiment_run_uid: str

              :returns: metric values
              :rtype: list

              A way you might use me is:

              >>> client.experiments.get_metrics(experiment_run_uid)
        """
        experiment_run_uid = str_type_conv(experiment_run_uid)
        Experiments._validate_type(experiment_run_uid, 'experiment_run_uid', STR_TYPE, True)

        training_statuses = self.get_run_details(experiment_run_uid)['entity']['training_statuses']

        metrics = []

        for status in training_statuses:
            training_guid_metrics = status['metrics']

            if len(training_guid_metrics) > 0:
                metrics.append({"training_guid": status['training_guid'], "training_reference_name": status['training_reference_name'], "metrics": training_guid_metrics})

        return metrics

