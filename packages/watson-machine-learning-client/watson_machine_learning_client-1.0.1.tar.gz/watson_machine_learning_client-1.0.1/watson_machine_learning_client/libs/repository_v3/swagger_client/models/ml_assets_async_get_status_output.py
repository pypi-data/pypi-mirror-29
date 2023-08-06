from pprint import pformat
from six import iteritems
import re

class MlAssetsAsyncGetStatusOutput(object):
    def __init__(self, jobId=None, statusMessage=None, statusURL=None):
        self.swagger_types = {
            'jobId': 'str',
            'statusMessage':'str',
            'statusURL':'str'

        }

        self.attribute_map = {
            'jobId': 'jobId',
            'statusMessage': 'statusMessage',
            'statusURL':'str'

        }

        self._jobId = jobId
        self._statusMessage = statusMessage
        self._statusURL = statusURL
    @property
    def jobId(self):

        return self._jobId

    @jobId.setter
    def jobId(self, jobId):

        self._jobId = jobId

    @property
    def statusMessage(self):

        return self._statusMessage

    @statusMessage.setter
    def statusMessage(self, statusMessage):

        self._statusMessage = statusMessage

    @property
    def statusURL(self):

        return self._statusURL

    @statusURL.setter
    def statusURL(self, statusURL):

        self._statusURL = statusURL

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
