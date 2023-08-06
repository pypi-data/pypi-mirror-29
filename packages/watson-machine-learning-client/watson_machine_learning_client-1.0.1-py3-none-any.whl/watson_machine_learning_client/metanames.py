################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
from repository_v3.mlrepository import MetaNames
from tabulate import tabulate
import json
from watson_machine_learning_client.wml_resource import WMLResource
from watson_machine_learning_client.utils import STR_TYPE, STR_TYPE_NAME


class ExperimentMetaNames:
    """
    Set of Meta Names for experiments.

    Available MetaNames:

    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | MetaName                                      | Type | Required | Example value                                                                                                                                                                                                                                        |
    +===============================================+======+==========+======================================================================================================================================================================================================================================================+
    | ExperimentMetaNames.NAME                      | str  | Y        | ``"Hand-written Digit Recognition"``                                                                                                                                                                                                                 |
    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ExperimentMetaNames.DESCRIPTION               | str  | N        | ``"Hand-written Digit Recognition training"``                                                                                                                                                                                                        |
    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ExperimentMetaNames.AUTHOR_NAME               | str  | N        | ``"John Smith"``                                                                                                                                                                                                                                     |
    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ExperimentMetaNames.AUTHOR_EMAIL              | str  | Y        | ``"John.Smith@x.x"``                                                                                                                                                                                                                                 |
    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ExperimentMetaNames.TAGS                      | list | N        | ``[{"value":"dsx-project.<project-guid>", "description": "DSX project guid"}]``                                                                                                                                                                                                                                 |
    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ExperimentMetaNames.EVALUATION_METHOD         | str  | N        | ``"multiclass"``                                                                                                                                                                                                                                     |
    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ExperimentMetaNames.EVALUATION_METRICS        | list | Y        | ``["accuracy"]``                                                                                                                                                                                                                                     |
    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ExperimentMetaNames.TRAINING_REFERENCES       | dict | Y        | ``[{"training_definition_url": "https://ibm-watson-ml.mybluemix.net/v3/ml_assets/training_definitions/12345"}, {"training_definition_url": "https://ibm-watson-ml.mybluemix.net/v3/ml_assets/training_definitions/67890"}]``         |
    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ExperimentMetaNames.TRAINING_DATA_REFERENCE   | dict | Y        | ``{"connection": {"endpoint_url": "https://s3-api.us-geo.objectstorage.softlayer.net", "access_key_id": "***", "secret_access_key": "***"}, "source": {"bucket": "train-data"}, "type": "s3"}``  |
    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ExperimentMetaNames.TRAINING_RESULTS_REFERENCE| dict | Y        | ``{"connection": {"endpoint_url": "https://s3-api.us-geo.objectstorage.softlayer.net", "access_key_id": "***", "secret_access_key": "***"}, "target": {"bucket": "result-data"}, "type": "s3"}`` |
    +-----------------------------------------------+------+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    """
    def __init__(self):
        self.NAME = u'name'
        self.DESCRIPTION = u'description'
        self.TAGS = u'tags'
        self.AUTHOR_NAME = u'author_name'
        self.AUTHOR_EMAIL = u'author_email'
        self.EVALUATION_METHOD = u'evaluation_method'
        self.EVALUATION_METRICS = u'evaluation_metrics'
        self.TRAINING_REFERENCES = u'training_references'
        self.TRAINING_DATA_REFERENCE = u'training_data_reference'
        self.TRAINING_RESULTS_REFERENCE = u'training_results_reference'

        self._NAME_REQUIRED = True
        self._TAGS_REQUIRED = False
        self._DESCRIPTION_REQUIRED = False
        self._AUTHOR_NAME_REQUIRED = False
        self._AUTHOR_EMAIL_REQUIRED = True
        self._EVALUATION_METHOD_REQUIRED = False
        self._EVALUATION_METRICS_REQUIRED = False
        self._TRAINING_REFERENCES_REQUIRED = True
        self._TRAINING_DATA_REFERENCE_REQUIRED = True
        self._TRAINING_RESULTS_REFERENCE_REQUIRED = True

    def _validate(self, meta_props):
        WMLResource._validate_meta_prop(meta_props, self.NAME, STR_TYPE, self._NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.DESCRIPTION, STR_TYPE, self._DESCRIPTION_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.TAGS, list, self._TAGS_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.AUTHOR_NAME, STR_TYPE, self._AUTHOR_NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.AUTHOR_EMAIL, STR_TYPE, self._AUTHOR_EMAIL_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.EVALUATION_METHOD, STR_TYPE, self._EVALUATION_METHOD_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.EVALUATION_METRICS, list, self._EVALUATION_METRICS_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.TRAINING_REFERENCES, list, self._TRAINING_REFERENCES_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.TRAINING_DATA_REFERENCE, dict, self._TRAINING_DATA_REFERENCE_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.TRAINING_RESULTS_REFERENCE, dict, self._TRAINING_RESULTS_REFERENCE_REQUIRED)

    def get(self):
        """
        Get available experiment metanames.

        :return: available experiment metanames
        :rtype: array
        """
        return sorted(list(filter(lambda x: not x.startswith('_'), self.__dict__.keys())))

    def show(self):
        """
        Shows possible metanames, type and if it is required.
        """
        table = tabulate(
            [
                [u'META_PROP NAME',               u'TYPE', u'REQUIRED'],
                [u'NAME',                         STR_TYPE_NAME,  u'Y' if self._NAME_REQUIRED else u'N'],
                [u'TAGS',                         u'list',        u'Y' if self._TAGS_REQUIRED else u'N'],
                [u'DESCRIPTION',                  STR_TYPE_NAME,  u'Y' if self._DESCRIPTION_REQUIRED else u'N'],
                [u'AUTHOR_NAME',                  STR_TYPE_NAME,  u'Y' if self._AUTHOR_NAME_REQUIRED else u'N'],
                [u'AUTHOR_EMAIL',                 STR_TYPE_NAME,  u'Y' if self._AUTHOR_EMAIL_REQUIRED else u'N'],
                [u'EVALUATION_METHOD',            STR_TYPE_NAME,  u'Y' if self._EVALUATION_METHOD_REQUIRED else u'N'],
                [u'EVALUATION_METRICS',           u'list', u'Y' if self._EVALUATION_METRICS_REQUIRED else u'N'],
                [u'TRAINING_REFERENCES',          u'list', u'Y' if self._TRAINING_REFERENCES_REQUIRED else u'N'],
                [u'TRAINING_DATA_REFERENCE',      u'dict', u'Y' if self._TRAINING_DATA_REFERENCE_REQUIRED else u'N'],
                [u'TRAINING_RESULTS_REFERENCE',   u'dict', u'Y' if self._TRAINING_RESULTS_REFERENCE_REQUIRED else u'N']
            ]
        )
        print(table)

    def get_example_values(self):
        """
        Get example values for metanames.

        :return: example meta_props
        :rtype: json
        """
        training_data_reference = {
            u'connection': {
                u'endpoint_url': u'https://s3-api.us-geo.objectstorage.softlayer.net',
                u'access_key_id': u'***',
                u'secret_access_key': u'***'
            },
            u'source': {
                u'bucket': u'train-data'
            },
            u'type': u's3'
        }

        training_results_reference = {
            u'connection': {
                u'endpoint_url': u'https://s3-api.us-geo.objectstorage.softlayer.net',
                u'access_key_id': u'***',
                u'secret_access_key': u'***'
            },
            u'target': {
                u'bucket': u'result-data'
            },
            u'type': 's3'
        }

        training_references = [
            {
                u'training_definition_url': u'https://ibm-watson-ml.mybluemix.net/v3/ml_assets/training_definitions/12345',
                u'compute_configuration': {u'name': u'small'}
            },
            {
                u'training_definition_url': u'https://ibm-watson-ml.mybluemix.net/v3/ml_assets/training_definitions/67890',
            }
        ]

        tags = [
                {
                    u'value': 'dsx-project.<project-guid>',
                    u'description': 'DSX project guid'
                }
        ]

        return {
            self.NAME: u'Hand-written Digit Recognitionu',
            self.DESCRIPTION: u'Hand-written Digit Recognition training',
            self.TAGS: tags,
            self.AUTHOR_NAME: u'John Smith',
            self.AUTHOR_EMAIL: u'John.Smith@ibm.com',
            self.EVALUATION_METHOD: u'multiclass',
            self.EVALUATION_METRICS: [u'accuracy'],
            self.TRAINING_REFERENCES: training_references,
            self.TRAINING_DATA_REFERENCE: training_data_reference,
            self.TRAINING_RESULTS_REFERENCE: training_results_reference
        }


class TrainingConfigurationMetaNames:
    """
    Set of Meta Names for trainings.

    Available MetaNames:

    +-----------------------------------------------------------+------+----------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | MetaName                                                  | Type | Required | Default value                 | Example value                                                                                                                                                                                                                                        |
    +===========================================================+======+==========+===============================+======================================================================================================================================================================================================================================================+
    | TrainingConfigurationMetaNames.NAME                       | str  | Y        |                               | ``"Hand-written Digit Recognition"``                                                                                                                                                                                                                 |
    +-----------------------------------------------------------+------+----------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | TrainingConfigurationMetaNames.DESCRIPTION                | str  | N        |                               | ``"Hand-written Digit Recognition training"``                                                                                                                                                                                                        |
    +-----------------------------------------------------------+------+----------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | TrainingConfigurationMetaNames.AUTHOR_NAME                | str  | N        |                               | ``"John Smith"``                                                                                                                                                                                                                                     |
    +-----------------------------------------------------------+------+----------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | TrainingConfigurationMetaNames.AUTHOR_EMAIL               | str  | Y        |                               | ``"John.Smith@x.x"``                                                                                                                                                                                                                                 |
    +-----------------------------------------------------------+------+----------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | TrainingConfigurationMetaNames.TRAINING_DATA_REFERENCE    | dict | Y        |                               | ``{"connection": {"auth_url": "https://identity.open.softlayer.com/v3", "user_name": "xxx", "password": "xxx", "region": "dallas", "domain_name": "xxx", "project_id": "xxx"}, "source": {"bucket": "train-data"}, "type": "bluemix_objectstore"}``  |
    +-----------------------------------------------------------+------+----------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | TrainingConfigurationMetaNames.TRAINING_RESULTS_REFERENCE | dict | Y        |                               | ``{"connection": {"auth_url": "https://identity.open.softlayer.com/v3", "user_name": "xxx", "password": "xxx", "region": "dallas", "domain_name": "xxx", "project_id": "xxx"}, "target": {"bucket": "result-data"}, "type": "bluemix_objectstore"}`` |
    +-----------------------------------------------------------+------+----------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | TrainingConfigurationMetaNames.EXECUTION_COMMAND          | str  | N        | <value from model definition> | ``"python3 tensorflow_mnist_softmax.py --trainingIters 20"``                                                                                                                                                                                         |
    +-----------------------------------------------------------+------+----------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | TrainingConfigurationMetaNames.COMPUTE_CONFIGURATION      | dict | N        | ``{"name":"small"}``          | ``{"name": "small", "nodes": 1}``                                                                                                                                                                                                                                          |
    +-----------------------------------------------------------+------+----------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

    """

    def __init__(self):
        self.NAME = u'name'
        self.DESCRIPTION = u'description'
        self.AUTHOR_NAME = u'author_name'
        self.AUTHOR_EMAIL = u'author_email'
        self.TRAINING_DATA_REFERENCE = u'training_data'
        self.TRAINING_RESULTS_REFERENCE = u'training_results'
        self.EXECUTION_COMMAND = u'command'
        self.COMPUTE_CONFIGURATION = u'compute_configuration_name'

        self._NAME_REQUIRED = True
        self._DESCRIPTION_REQUIRED = False
        self._AUTHOR_NAME_REQUIRED = False
        self._AUTHOR_EMAIL_REQUIRED = True
        self._TRAINING_DATA_REFERENCE_REQUIRED = True
        self._TRAINING_RESULTS_REFERENCE_REQUIRED = True
        self._EXECUTION_COMMAND_REQUIRED = False
        self._COMPUTE_CONFIGURATION_REQUIRED = False

    def _validate(self, meta_props):
        WMLResource._validate_meta_prop(meta_props, self.NAME, STR_TYPE, self._NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.DESCRIPTION, STR_TYPE, self._DESCRIPTION_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.AUTHOR_NAME, STR_TYPE, self._AUTHOR_NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.AUTHOR_EMAIL, STR_TYPE, self._AUTHOR_EMAIL_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.TRAINING_DATA_REFERENCE, dict, self._TRAINING_DATA_REFERENCE_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.TRAINING_RESULTS_REFERENCE, dict, self._TRAINING_RESULTS_REFERENCE_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.EXECUTION_COMMAND, STR_TYPE, self._EXECUTION_COMMAND_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.COMPUTE_CONFIGURATION, dict, self._COMPUTE_CONFIGURATION_REQUIRED)

    def get(self):
        """
        Get available experiment metanames.

        :return: available experiment metanames
        :rtype: array
        """
        return sorted(list(filter(lambda x: not x.startswith('_'), self.__dict__.keys())))

    def show(self):
        """
            Shows possible metanames, type and if it is required.
        """
        table = tabulate(
            [
                [u'META_PROP NAME',                  u'TYPE',     u'REQUIRED',                                                 u'DEFAULT VALUE'],
                [u'NAME',                         STR_TYPE_NAME,      u'Y' if self._NAME_REQUIRED else u'N',                        u''],
                [u'DESCRIPTION',                  STR_TYPE_NAME,      u'Y' if self._DESCRIPTION_REQUIRED else u'N',                 u''],
                [u'AUTHOR_NAME',                  STR_TYPE_NAME,      u'Y' if self._AUTHOR_NAME_REQUIRED else u'N',                 u''],
                [u'AUTHOR_EMAIL',                 STR_TYPE_NAME,      u'Y' if self._AUTHOR_EMAIL_REQUIRED else u'N',                u''],
                [u'TRAINING_DATA_REFERENCE',      u'dict',            u'Y' if self._TRAINING_DATA_REFERENCE_REQUIRED else u'N',     u''],
                [u'TRAINING_RESULTS_REFERENCE',   u'dict',            u'Y' if self._TRAINING_RESULTS_REFERENCE_REQUIRED else u'N',  u''],
                [u'EXECUTION_COMMAND',            STR_TYPE_NAME,      u'Y' if self._EXECUTION_COMMAND_REQUIRED else u'N',           u'<value from model definition>'],
                [u'COMPUTE_CONFIGURATION',        u'dict',            u'Y' if self._COMPUTE_CONFIGURATION_REQUIRED else u'N',     u'small']
            ]
        )
        print(table)

    def get_example_values(self):
        """
        Get example values for metanames.

        :return: example meta_props
        :rtype: json
        """
        training_data_reference = {
            u'connection': {
                u'endpoint_url': u'https://s3-api.us-geo.objectstorage.softlayer.net',
                u'access_key_id': u'***',
                u'secret_access_key': u'***'
            },
            u'source': {
                u'bucket': u'train-data'
            },
            u'type': u's3'
        }

        training_results_reference = {
            u'connection': {
                u'endpoint_url': u'https://s3-api.us-geo.objectstorage.softlayer.net',
                u'access_key_id': u'***',
                u'secret_access_key': u'***'
            },
            u'target': {
                u'bucket': u'train-data'
            },
            u'type': u's3'
        }

        return {
            self.NAME: u'Hand-written Digit Recognition',
            self.DESCRIPTION: u'Hand-written Digit Recognition training',
            self.AUTHOR_NAME: u'John Smith',
            self.AUTHOR_EMAIL: u'John.Smith@x.x',
            self.TRAINING_DATA_REFERENCE: training_data_reference,
            self.TRAINING_RESULTS_REFERENCE: training_results_reference,
            self.EXECUTION_COMMAND: u'python3 tensorflow_mnist_softmax.py --trainingIters 20',
            self.COMPUTE_CONFIGURATION: {u'name': u'p100'}
        }


class ModelDefinitionMetaNames:
    """
    Set of Meta Names for model definitions.

    Available MetaNames:

    +---------------------------------------------+------+----------+--------------------------------------------------------------+
    | MetaName                                    | Type | Required | Example value                                                |
    +=============================================+======+==========+==============================================================+
    | ModelDefinitionMetaNames.NAME               | str  | Y        | ``"Hand-written Digit Recognition"``                         |
    +---------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.DESCRIPTION        | str  | N        | ``"Hand-written Digit Recognition training"``                |
    +---------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.AUTHOR_NAME        | str  | N        | ``"John Smith"``                                             |
    +---------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.AUTHOR_EMAIL       | str  | Y        | ``"John.Smith@ibm.com"``                                         |
    +---------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.FRAMEWORK_NAME     | str  | Y        | ``"tensorflow"``                                             |
    +---------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.FRAMEWORK_VERSION  | str  | Y        | ``"1.5"``                                                    |
    +---------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.RUNTIME_NAME       | str  | Y        | ``"python"``                                                 |
    +---------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.RUNTIME_VERSION    | str  | Y        | ``"3.5"``                                                    |
    +---------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.EXECUTION_COMMAND  | str  | Y        | ``"python3 tensorflow_mnist_softmax.py --trainingIters 20"`` |
    +---------------------------------------------+------+----------+--------------------------------------------------------------+
    """

    def __init__(self):
        self.NAME = u'name'
        self.DESCRIPTION = u'description'
        self.AUTHOR_NAME = u'author_name'
        self.AUTHOR_EMAIL = u'author_email'
        self.FRAMEWORK_NAME = u'framework_name'
        self.FRAMEWORK_VERSION = u'framework_version'
        self.RUNTIME_NAME = u'runtime_name'
        self.RUNTIME_VERSION = u'runtime_version'
        self.EXECUTION_COMMAND = u'command'

        self._NAME_REQUIRED = True
        self._DESCRIPTION_REQUIRED = False
        self._AUTHOR_NAME_REQUIRED = False
        self._AUTHOR_EMAIL_REQUIRED = True
        self._FRAMEWORK_NAME_REQUIRED = True
        self._FRAMEWORK_VERSION_REQUIRED = True
        self._RUNTIME_NAME_REQUIRED = True
        self._RUNTIME_VERSION_REQUIRED = True
        self._EXECUTION_COMMAND_REQUIRED = True

    def _validate(self, meta_props):
        WMLResource._validate_meta_prop(meta_props, self.NAME, STR_TYPE, self._NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.DESCRIPTION, STR_TYPE, self._DESCRIPTION_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.AUTHOR_NAME, STR_TYPE, self._AUTHOR_NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.AUTHOR_EMAIL, STR_TYPE, self._AUTHOR_EMAIL_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.FRAMEWORK_NAME, STR_TYPE, self._FRAMEWORK_NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.FRAMEWORK_VERSION, STR_TYPE, self._FRAMEWORK_VERSION_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.RUNTIME_NAME, STR_TYPE, self._RUNTIME_NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.RUNTIME_VERSION, STR_TYPE, self._RUNTIME_VERSION_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.EXECUTION_COMMAND, STR_TYPE, self._EXECUTION_COMMAND_REQUIRED)

    def get(self):
        """
        Get available experiment metanames.

        :return: available experiment metanames
        :rtype: array
        """
        return sorted(list(filter(lambda x: not x.startswith('_'), self.__dict__.keys())))

    def show(self):
        """
            Shows possible metanames, type and if it is required.
        """
        table = tabulate(
            [
                [u'META_PROP NAME',          u'TYPE', u'REQUIRED'],
                [u'NAME',                 STR_TYPE_NAME,  u'Y' if self._NAME_REQUIRED else u'N'],
                [u'DESCRIPTION',          STR_TYPE_NAME,  u'Y' if self._DESCRIPTION_REQUIRED else u'N'],
                [u'AUTHOR_NAME',          STR_TYPE_NAME,  u'Y' if self._AUTHOR_NAME_REQUIRED else u'N'],
                [u'AUTHOR_EMAIL',         STR_TYPE_NAME,  u'Y' if self._AUTHOR_EMAIL_REQUIRED else u'N'],
                [u'FRAMEWORK_NAME',       STR_TYPE_NAME,  u'Y' if self._FRAMEWORK_NAME_REQUIRED else u'N'],
                [u'FRAMEWORK_VERSION',    STR_TYPE_NAME,  u'Y' if self._FRAMEWORK_VERSION_REQUIRED else u'N'],
                [u'RUNTIME_NAME',         STR_TYPE_NAME,  u'Y' if self._RUNTIME_NAME_REQUIRED else u'N'],
                [u'RUNTIME_VERSION',      STR_TYPE_NAME,  u'Y' if self._RUNTIME_VERSION_REQUIRED else u'N'],
                [u'EXECUTION_COMMAND',    STR_TYPE_NAME,  u'Y' if self._EXECUTION_COMMAND_REQUIRED else u'N']
            ]
        )
        print(table)

    def get_example_values(self):
        """
            Get example values for metanames.

            :return: example meta_props
            :rtype: json
        """
        return {
            self.NAME: u'my_training_definition',
            self.DESCRIPTION: u'my_description',
            self.AUTHOR_NAME: u'John Smith',
            self.AUTHOR_EMAIL: u'John.Smith@ibm.com',
            self.FRAMEWORK_NAME: u'tensorflow',
            self.FRAMEWORK_VERSION: u'1.5',
            self.RUNTIME_NAME: u'python',
            self.RUNTIME_VERSION: u'3.5',
            self.EXECUTION_COMMAND: u'python3 tensorflow_mnist_softmax.py --trainingIters 20'
        }


class ModelMetaNames:
    """
    Set of Meta Names for models.

    Available MetaNames:

    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | MetaName                                         | Type | Required | Example value                                                |
    +==================================================+======+==========+==============================================================+
    | ModelDefinitionMetaNames.NAME                    | str  | Y        | ``"my_model"``                                               |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.DESCRIPTION             | str  | N        | ``"my_description"``                                         |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.AUTHOR_NAME             | str  | N        | ``"John Smith"``                                             |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.AUTHOR_EMAIL            | str  | N        | ``"John.Smith@x.x"``                                         |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.FRAMEWORK_NAME          | str  | N        | ``"tensorflow"``                                             |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.FRAMEWORK_VERSION       | str  | N        | ``"1.5"``                                                    |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.FRAMEWORK_LIBRARIES     | list | N        | [{"name": "keras", "version": "2.1.3"}]                      |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.RUNTIME_NAME            | str  | N        | ``"python"``                                                 |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.RUNTIME_VERSION         | str  | N        | ``"3.5"``                                                    |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.TRAINING_DATA_REFERENCE | json | N        | ``"{}"``                                                     |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.EVALUATION_METHOD       | str  | N        | ``"multiclass"``                                             |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | ModelDefinitionMetaNames.EVALUATION_METRICS      | list | N        | ``[{"name": "accuracy", "value": 0.64, "threshold": 0.8}]``  |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    """

    def __init__(self):
        self.NAME = u'name'
        self.DESCRIPTION = MetaNames.DESCRIPTION
        self.AUTHOR_NAME = MetaNames.AUTHOR_NAME
        self.AUTHOR_EMAIL = MetaNames.AUTHOR_EMAIL
        self.FRAMEWORK_NAME = MetaNames.FRAMEWORK_NAME
        self.FRAMEWORK_VERSION = MetaNames.FRAMEWORK_VERSION
        self.FRAMEWORK_LIBRARIES = MetaNames.FRAMEWORK_LIBRARIES
        self.RUNTIME_NAME = u'runtime_name'
        self.RUNTIME_VERSION = u'runtime_version'
        self.TRAINING_DATA_REFERENCE = MetaNames.TRAINING_DATA_REFERENCE
        self.EVALUATION_METHOD = MetaNames.EVALUATION_METHOD
        self.EVALUATION_METRICS = MetaNames.EVALUATION_METRICS

        self._NAME_REQUIRED = True
        self._DESCRIPTION_REQUIRED = False
        self._AUTHOR_NAME_REQUIRED = False
        self._AUTHOR_EMAIL_REQUIRED = False
        self._FRAMEWORK_NAME_REQUIRED = False
        self._FRAMEWORK_VERSION_REQUIRED = False
        self._FRAMEWORK_LIBRARIES_REQUIRED = False
        self._RUNTIME_NAME_REQUIRED = False
        self._RUNTIME_VERSION_REQUIRED = False
        self._TRAINING_DATA_REFERENCE_REQUIRED = False
        self._EVALUATION_METHOD_REQUIRED = False
        self._EVALUATION_METRICS_REQUIRED = False


    def _validate(self, meta_props):
        WMLResource._validate_meta_prop(meta_props, self.NAME, STR_TYPE, self._NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.DESCRIPTION, STR_TYPE, self._DESCRIPTION_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.AUTHOR_NAME, STR_TYPE, self._AUTHOR_NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.AUTHOR_EMAIL, STR_TYPE, self._AUTHOR_EMAIL_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.FRAMEWORK_NAME, STR_TYPE, self._FRAMEWORK_NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.FRAMEWORK_VERSION, STR_TYPE, self._FRAMEWORK_VERSION_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.FRAMEWORK_LIBRARIES, list, self._FRAMEWORK_LIBRARIES_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.RUNTIME_NAME, STR_TYPE, self._RUNTIME_NAME_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.RUNTIME_VERSION, STR_TYPE, self._RUNTIME_VERSION_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.TRAINING_DATA_REFERENCE, dict, self._TRAINING_DATA_REFERENCE_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.EVALUATION_METHOD, STR_TYPE, self._EVALUATION_METHOD_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.EVALUATION_METRICS, list, self._EVALUATION_METRICS_REQUIRED)

    def get(self):
        """
        Get available experiment metanames.

        :return: available experiment metanames
        :rtype: array
        """
        return sorted(list(filter(lambda x: not x.startswith('_'), self.__dict__.keys())))

    def show(self):
        """
            Shows possible metanames, type and if it is required.
        """
        table = tabulate(
            [
                [u'META_PROP NAME',          u'TYPE',        u'REQUIRED'],
                [u'NAME',                    STR_TYPE_NAME,  u'Y' if self._NAME_REQUIRED else u'N'],
                [u'DESCRIPTION',             STR_TYPE_NAME,  u'Y' if self._DESCRIPTION_REQUIRED else u'N'],
                [u'AUTHOR_NAME',             STR_TYPE_NAME,  u'Y' if self._AUTHOR_NAME_REQUIRED else u'N'],
                [u'AUTHOR_EMAIL',            STR_TYPE_NAME,  u'Y' if self._AUTHOR_EMAIL_REQUIRED else u'N'],
                [u'FRAMEWORK_NAME',          STR_TYPE_NAME,  u'Y' if self._FRAMEWORK_NAME_REQUIRED else u'N'],
                [u'FRAMEWORK_VERSION',       STR_TYPE_NAME,  u'Y' if self._FRAMEWORK_VERSION_REQUIRED else u'N'],
                [u'FRAMEWORK_LIBRARIES',     u'list',        u'Y' if self._FRAMEWORK_LIBRARIES_REQUIRED else u'N'],
                [u'RUNTIME_NAME',            STR_TYPE_NAME,  u'Y' if self._RUNTIME_NAME_REQUIRED else u'N'],
                [u'RUNTIME_VERSION',         STR_TYPE_NAME,  u'Y' if self._RUNTIME_VERSION_REQUIRED else u'N'],
                [u'TRAINING_DATA_REFERENCE', u'dict',        u'Y' if self._TRAINING_DATA_REFERENCE_REQUIRED else u'N'],
                [u'EVALUATION_METHOD',       STR_TYPE_NAME,  u'Y' if self._EVALUATION_METHOD_REQUIRED else u'N'],
                [u'EVALUATION_METRICS',      u'list',        u'Y' if self._EVALUATION_METRICS_REQUIRED else u'N']
            ]
        )
        print(table)

    def get_example_values(self):
        """
            Get example values for metanames.

            :return: example meta_props
            :rtype: json
        """
        return {
            self.NAME: "my_model",
            self.DESCRIPTION: "my_description",
            self.AUTHOR_NAME: "John Smith",
            self.AUTHOR_EMAIL: "John.Smith@ibm.com",
            self.FRAMEWORK_NAME: "tensorflow",
            self.FRAMEWORK_VERSION: "1.5",
            self.FRAMEWORK_LIBRARIES: [{'name': 'keras', 'version': '2.1.3'}],
            self.RUNTIME_NAME: "python",
            self.RUNTIME_VERSION: "3.5",
            self.TRAINING_DATA_REFERENCE: {},
            self.EVALUATION_METHOD: "multiclass",
            self.EVALUATION_METRICS: [
                {
                    "name": "accuracy",
                    "value": 0.64,
                    "threshold": 0.8
                }
            ]
        }


class LearningSystemMetaNames:
    """
    Set of Meta Names for learning system.

    Available MetaNames:

    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | MetaName                                         | Type | Required | Example value                                                |
    +==================================================+======+==========+==============================================================+
    | LearningSystemMetaNames.FEEDBACK_DATA_REFERENCE  | json | Y        | ``"{}"``                                                     |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | LearningSystemMetaNames.SPARK_REFERENCE          | json | Y        | ``"{}"``                                                     |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | LearningSystemMetaNames.MIN_FEEDBACK_DATA_SIZE   | int  | Y        | ``1000``                                                     |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | LearningSystemMetaNames.AUTO_RETRAIN             | str  | Y        | ``"always"``                                         |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    | LearningSystemMetaNames.AUTO_REDEPLOY            | str  | Y        | ``"never"``                                             |
    +--------------------------------------------------+------+----------+--------------------------------------------------------------+
    """

    def __init__(self):
        self.FEEDBACK_DATA_REFERENCE = "feedback_data_reference"
        self.SPARK_REFERENCE = "spark_instance"
        self.MIN_FEEDBACK_DATA_SIZE = "min_feedback_data_size"
        self.AUTO_RETRAIN = "auto_retrain"
        self.AUTO_REDEPLOY = "auto_redeploy"

        self._FEEDBACK_DATA_REFERENCE_REQUIRED = True
        self._MIN_FEEDBACK_DATA_SIZE_REQUIRED = True
        self._SPARK_REFERENCE_REQUIRED = True
        self._AUTO_RETRAIN_REQUIRED = True
        self._AUTO_REDEPLOY_REQUIRED = True

    def _validate(self, meta_props):
        WMLResource._validate_meta_prop(meta_props, self.FEEDBACK_DATA_REFERENCE, dict, self._FEEDBACK_DATA_REFERENCE_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.SPARK_REFERENCE, dict, self._SPARK_REFERENCE_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.MIN_FEEDBACK_DATA_SIZE, int, self._MIN_FEEDBACK_DATA_SIZE_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.AUTO_RETRAIN, STR_TYPE, self._AUTO_RETRAIN_REQUIRED)
        WMLResource._validate_meta_prop(meta_props, self.AUTO_REDEPLOY, STR_TYPE, self._AUTO_REDEPLOY_REQUIRED)

    def get(self):
        """
        Get available continuous learning system metanames.

        :return: available learning system metanames
        :rtype: array
        """
        return sorted(list(filter(lambda x: not x.startswith('_'), self.__dict__.keys())))

    def show(self):
        """
            Shows possible metanames, type and if it is required.
        """
        table = tabulate(
            [
                ["META_PROP NAME",                  "TYPE", "REQUIRED"],
                ["FEEDBACK_DATA_REFERENCE",         "json", "Y" if self._FEEDBACK_DATA_REFERENCE_REQUIRED else "N"],
                ["SPARK_REFERENCE",                 "json", "Y" if self._SPARK_REFERENCE_REQUIRED else "N"],
                ["MIN_FEEDBACK_DATA_SIZE_REQUIRED", "int",  "Y" if self._MIN_FEEDBACK_DATA_SIZE_REQUIRED else "N"],
                ["AUTO_RETRAIN",                    "str",  "Y" if self._AUTO_RETRAIN_REQUIRED else "N"],
                ["AUTO_REDEPLOY",                   "str",  "Y" if self._AUTO_REDEPLOY_REQUIRED else "N"],
            ]
        )
        print(table)

    def get_example_values(self):
        """
            Get example values for metanames.

            :return: example meta_props
            :rtype: json
        """
        return {
            self.FEEDBACK_DATA_REFERENCE: {},
            self.MIN_FEEDBACK_DATA_SIZE: 100,
            self.SPARK_REFERENCE: {},
            self.AUTO_RETRAIN: "conditionally",
            self.AUTO_REDEPLOY: "always"
        }
