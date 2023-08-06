################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
from watson_machine_learning_client.wml_client_error import ApiRequestFailure, WMLClientError
from watson_machine_learning_client.href_definitions import HrefDefinitions
import re
import os
import sys

INSTANCE_DETAILS_TYPE = u'instance_details_type'
DEPLOYMENT_DETAILS_TYPE = u'deployment_details_type'
EXPERIMENT_RUN_DETAILS_TYPE = u'experiment_run_details_type'
MODEL_DETAILS_TYPE = u'model_details_type'
DEFINITION_DETAILS_TYPE = u'definition_details_type'
EXPERIMENT_DETAILS_TYPE = u'experiment_details_type'
TRAINING_RUN_DETAILS_TYPE = u'training_run_details_type'

UNKNOWN_ARRAY_TYPE = u'resource_type'
UNKNOWN_TYPE = u'unknown_type'

SPARK_MLLIB = u'mllib'
SPSS_FRAMEWORK = u'spss-modeler'
TENSORFLOW_FRAMEWORK = u'tensorflow'
XGBOOST_FRAMEWORK = u'xgboost'
SCIKIT_LEARN_FRAMEWORK = u'scikit-learn'
PMML_FRAMEWORK = u'pmml'

STR_TYPE = type(u'string or unicode')
STR_TYPE_NAME = STR_TYPE.__name__


def is_python_2():
    return sys.version_info[0] == 2


def str_type_conv(string):
    if is_python_2() and type(string) is str:
        return unicode(string)
    else:
        return string


def meta_props_str_conv(meta_props):
    for key in meta_props:
        if is_python_2() and type(meta_props[key]) is str:
            meta_props[key] = unicode(meta_props[key])


def get_ml_token(watson_ml_creds):
    import requests
    import json

    if u'ml_token' not in watson_ml_creds:
        response = requests.get(HrefDefinitions(watson_ml_creds).get_token_endpoint_href(), auth=(watson_ml_creds[u'username'], watson_ml_creds[u'password']))
        if response.status_code == 200:
            watson_ml_creds[u'ml_token'] = json.loads(response.text).get(u'token')
        else:
            raise ApiRequestFailure(u'Error during getting ML Token.', response)
    return watson_ml_creds[u'ml_token']

def get_url(url, headers, params=None):
    import requests

    return requests.get(url, headers=headers, params=params)

def get_headers(wml_token):
    return {u'Content-Type': u'application/json', u'Authorization': u'Bearer ' + wml_token}


def print_text_header_h1(title):
    title = str_type_conv(title)
    print(u'\n\n' + (u'#' * len(title)) + u'\n')
    print(title)
    print(u'\n' + (u'#' * len(title)) + u'\n\n')


def print_text_header_h2(title):
    title = str_type_conv(title)
    print(u'\n\n' + (u'-' * len(title)))
    print(title)
    print((u'-' * len(title)) + u'\n\n')


def get_type_of_details(details):
    if 'resources' in details:
        return UNKNOWN_ARRAY_TYPE
    else:
        try:
            if re.search(u'\/v3\/wml_instances\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return INSTANCE_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/published_models\/[^\/]+/deployments/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return DEPLOYMENT_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/v3\/experiments\/[^\/]+/runs/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return EXPERIMENT_RUN_DETAILS_TYPE
        except:
            pass

        try:
            if re.search('\/published_models\/[^\/]+$', details[u'metadata'][u'url']) is not None or re.search(u'\/v3\/ml_assets\/models\/[^\/]+$', details['entity']['ml_asset_url']) is not None:
                return MODEL_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/v3\/ml_assets\/training_definitions\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return DEFINITION_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/v3\/experiments\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return EXPERIMENT_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/v3\/models\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return TRAINING_RUN_DETAILS_TYPE
        except:
            pass

        return UNKNOWN_TYPE


def pack(directory_path):
    pass


def unpack(filename):
    pass


def load_model_from_directory(framework, directory_path):
    if framework == SPARK_MLLIB:
        from pyspark.ml import PipelineModel
        return PipelineModel.read().load(directory_path)
    elif framework == SPSS_FRAMEWORK:
        pass
    elif framework == TENSORFLOW_FRAMEWORK:
        pass
    elif framework == SCIKIT_LEARN_FRAMEWORK or framework == XGBOOST_FRAMEWORK:
        from sklearn.externals import joblib
        model_id = directory_path[directory_path.rfind('/') + 1:] + ".pkl"
        return joblib.load(os.path.join(directory_path, model_id))
    elif framework == PMML_FRAMEWORK:
        pass
    else:
        raise WMLClientError(u'Invalid framework specified: \'{}\'.'.format(framework))


# def load_model_from_directory(framework, directory_path):
#     if framework == SPARK_MLLIB:
#         from pyspark.ml import PipelineModel
#         return PipelineModel.read().load(directory_path)
#     elif framework == SPSS_FRAMEWORK:
#         pass
#     elif framework == TENSORFLOW_FRAMEWORK:
#         pass
#     elif framework == SCIKIT_LEARN_FRAMEWORK or framework == XGBOOST_FRAMEWORK:
#         from sklearn.externals import joblib
#         model_id = directory_path[directory_path.rfind('/') + 1:] + ".pkl"
#         return joblib.load(os.path.join(directory_path, model_id))
#     elif framework == PMML_MODEL:
#         pass
#     else:
#         raise WMLClientError('Invalid framework specified: \'{}\'.'.format(framework))


def load_model_from_package(framework, directory):
    unpack(directory)
    load_model_from_directory(framework, directory)


def save_model_to_file(model, framework, base_path, filename):
    if filename.find('.') != -1:
        base_name = filename[:filename.find('.') + 1]
        file_extension = filename[filename.find('.'):]
    else:
        base_name = filename
        file_extension = 'tar.gz'

    if framework == SPARK_MLLIB:
        model.write.overwrite.save(os.path.join(base_path, base_name))
    elif framework == SPSS_FRAMEWORK:
        pass
    elif framework == TENSORFLOW_FRAMEWORK:
        pass
    elif framework == XGBOOST_FRAMEWORK:
        pass
    elif framework == SCIKIT_LEARN_FRAMEWORK:
        os.makedirs(os.path.join(base_path, base_name))
        from sklearn.externals import joblib
        joblib.dump(model, os.path.join(base_path, base_name, base_name + ".pkl"))
    elif framework == PMML_FRAMEWORK:
        pass
    else:
        raise WMLClientError(u'Invalid framework specified: \'{}\'.'.format(framework))


def format_metrics(latest_metrics_list):
    formatted_metrics = u''

    for i in latest_metrics_list:

        values = i[u'values']

        if len(values) > 0:
            sorted_values = sorted(values, key=lambda k: k[u'name'])
        else:
            sorted_values = values

        for j in sorted_values:
            formatted_metrics = formatted_metrics + i[u'phase'] + ':' + j[u'name']+'='+'{0:.4f}'.format(j[u'value']) + '\n'

    return formatted_metrics


def docstring_parameter(args):
    def dec(obj):
        #obj.__doc__ = obj.__doc__.format(**args)
        return obj
    return dec


def group_metrics(metrics):
    grouped_metrics = []

    if len(metrics) > 0:
        import collections
        grouped_metrics = collections.defaultdict(list)
        for d in metrics:
            k = d[u'phase']
            grouped_metrics[k].append(d)

    return grouped_metrics
