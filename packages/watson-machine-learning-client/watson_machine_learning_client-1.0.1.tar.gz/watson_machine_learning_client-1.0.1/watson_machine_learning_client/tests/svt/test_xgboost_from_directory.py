import unittest
import os
import xgboost as xgb
from preparation_and_cleaning import *
from models_preparation import *
from watson_machine_learning_client.log_util import get_logger


class TestWMLClientWithXGBoost(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    scoring_url = None
    logger = get_logger(__name__)

    @classmethod
    def setUpClass(self):
        TestWMLClientWithXGBoost.logger.info("Service Instance: setting up credentials")
        self.wml_credentials = get_wml_credentials()
        self.client = get_client()
        self.model_path = os.path.join(os.getcwd(), 'artifacts', 'xgboost_model')

    def test_1_service_instance_details(self):
        TestWMLClientWithXGBoost.logger.info("Check client ...")
        self.assertTrue(self.client.__class__.__name__ == 'WatsonMachineLearningAPIClient')

        TestWMLClientWithXGBoost.logger.info("Getting instance details ...")
        details = self.client.service_instance.get_details()

        TestWMLClientWithXGBoost.logger.debug(details)
        self.assertTrue("published_models" in str(details))
        self.assertEqual(type(details), dict)

    def test_2_publish_model(self):
        TestWMLClientWithXGBoost.logger.info("Publishing xgboost model ...")
        import shutil

        try:
            shutil.rmtree(self.model_path)
        except:
            pass

        create_xgboost_model_directory(self.model_path)

        self.client.repository.ModelMetaNames.show()

        model_props = {self.client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                       self.client.repository.ModelMetaNames.AUTHOR_EMAIL: "ibm@ibm.com",
                       self.client.repository.ModelMetaNames.NAME: "LOCALLY created agaricus prediction model",
                       self.client.repository.ModelMetaNames.FRAMEWORK_NAME: "xgboost"
                       }
        published_model = self.client.repository.store_model(model=self.model_path, meta_props=model_props)
        TestWMLClientWithXGBoost.model_uid = self.client.repository.get_model_uid(published_model)
        TestWMLClientWithXGBoost.logger.info("Published model ID:" + str(TestWMLClientWithXGBoost.model_uid))
        self.assertIsNotNone(TestWMLClientWithXGBoost.model_uid)


        shutil.rmtree(self.model_path)

    def test_3_publish_model_details(self):
        TestWMLClientWithXGBoost.logger.info("Get published model details ...")
        details = self.client.repository.get_details(self.model_uid)

        TestWMLClientWithXGBoost.logger.debug("Model details: " + str(details))
        self.assertTrue("LOCALLY created agaricus prediction model" in str(details))

    def test_4_create_deployment(self):
        TestWMLClientWithXGBoost.logger.info("Create deployment ...")
        deployment = self.client.deployments.create(self.model_uid, "Test deployment", asynchronous=False)

        TestWMLClientWithXGBoost.logger.info("model_uid: " + self.model_uid)
        TestWMLClientWithXGBoost.logger.debug("Online deployment: " + str(deployment))
        TestWMLClientWithXGBoost.scoring_url = self.client.deployments.get_scoring_url(deployment)
        TestWMLClientWithXGBoost.deployment_uid = self.client.deployments.get_uid(deployment)
        self.assertTrue("online" in str(deployment))

    def test_5_get_deployment_details(self):
        TestWMLClientWithXGBoost.logger.info("Get deployment details ...")
        deployment_details = self.client.deployments.get_details()

        TestWMLClientWithXGBoost.logger.debug("Online deployment: " + str(deployment_details))
        self.assertTrue("Test deployment" in str(deployment_details))

    def test_6_score(self):
        TestWMLClientWithXGBoost.logger.info("Online model scoring ...")
        scoring_data = {
            'fields': ['f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'f14',
                       'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28',
                       'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42',
                       'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56',
                       'f57', 'f58', 'f59', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 'f69', 'f70',
                       'f71', 'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f79', 'f80', 'f81', 'f82', 'f83', 'f84',
                       'f85', 'f86', 'f87', 'f88', 'f89', 'f90', 'f91', 'f92', 'f93', 'f94', 'f95', 'f96', 'f97', 'f98',
                       'f99', 'f100', 'f101', 'f102', 'f103', 'f104', 'f105', 'f106', 'f107', 'f108', 'f109', 'f110',
                       'f111', 'f112', 'f113', 'f114', 'f115', 'f116', 'f117', 'f118', 'f119', 'f120', 'f121', 'f122',
                       'f123', 'f124', 'f125', 'f126'],
            'values': [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0,
                        0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                        0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0,
                        1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                        0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                        0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]}
        print(TestWMLClientWithXGBoost.scoring_url)
        predictions = self.client.deployments.score(TestWMLClientWithXGBoost.scoring_url, scoring_data)
        TestWMLClientWithXGBoost.logger.debug("Prediction: " + str(predictions))
        self.assertTrue("prediction" in predictions["fields"] or "probability" in predictions["fields"])

    def test_7_delete_deployment(self):
        TestWMLClientWithXGBoost.logger.info("Delete model deployment ...")
        self.client.deployments.delete(TestWMLClientWithXGBoost.deployment_uid)

    def test_8_delete_model(self):
        TestWMLClientWithXGBoost.logger.info("Delete model ...")
        self.client.repository.delete(TestWMLClientWithXGBoost.model_uid)


if __name__ == '__main__':
    unittest.main()
