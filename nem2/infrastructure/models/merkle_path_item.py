# coding: utf-8

"""
    Catapult REST API Reference

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.12
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MerklePathItem(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'position': 'int',
        'hash': 'str'
    }

    attribute_map = {
        'position': 'position',
        'hash': 'hash'
    }

    def __init__(self, position=None, hash=None):  # noqa: E501
        """MerklePathItem - a model defined in Swagger"""  # noqa: E501

        self._position = None
        self._hash = None
        self.discriminator = None

        if position is not None:
            self.position = position
        if hash is not None:
            self.hash = hash

    @property
    def position(self):
        """Gets the position of this MerklePathItem.  # noqa: E501


        :return: The position of this MerklePathItem.  # noqa: E501
        :rtype: int
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this MerklePathItem.


        :param position: The position of this MerklePathItem.  # noqa: E501
        :type: int
        """

        self._position = position

    @property
    def hash(self):
        """Gets the hash of this MerklePathItem.  # noqa: E501


        :return: The hash of this MerklePathItem.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this MerklePathItem.


        :param hash: The hash of this MerklePathItem.  # noqa: E501
        :type: str
        """

        self._hash = hash

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(MerklePathItem, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MerklePathItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
