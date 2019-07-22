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

from swagger_client.models.u_int64_dto import UInt64DTO  # noqa: F401,E501


class TransactionStatusDTO(object):
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
        'group': 'str',
        'status': 'str',
        'hash': 'str',
        'deadline': 'UInt64DTO',
        'height': 'UInt64DTO'
    }

    attribute_map = {
        'group': 'group',
        'status': 'status',
        'hash': 'hash',
        'deadline': 'deadline',
        'height': 'height'
    }

    def __init__(self, group=None, status=None, hash=None, deadline=None, height=None):  # noqa: E501
        """TransactionStatusDTO - a model defined in Swagger"""  # noqa: E501

        self._group = None
        self._status = None
        self._hash = None
        self._deadline = None
        self._height = None
        self.discriminator = None

        if group is not None:
            self.group = group
        self.status = status
        if hash is not None:
            self.hash = hash
        if deadline is not None:
            self.deadline = deadline
        if height is not None:
            self.height = height

    @property
    def group(self):
        """Gets the group of this TransactionStatusDTO.  # noqa: E501


        :return: The group of this TransactionStatusDTO.  # noqa: E501
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this TransactionStatusDTO.


        :param group: The group of this TransactionStatusDTO.  # noqa: E501
        :type: str
        """

        self._group = group

    @property
    def status(self):
        """Gets the status of this TransactionStatusDTO.  # noqa: E501


        :return: The status of this TransactionStatusDTO.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TransactionStatusDTO.


        :param status: The status of this TransactionStatusDTO.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def hash(self):
        """Gets the hash of this TransactionStatusDTO.  # noqa: E501


        :return: The hash of this TransactionStatusDTO.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this TransactionStatusDTO.


        :param hash: The hash of this TransactionStatusDTO.  # noqa: E501
        :type: str
        """

        self._hash = hash

    @property
    def deadline(self):
        """Gets the deadline of this TransactionStatusDTO.  # noqa: E501


        :return: The deadline of this TransactionStatusDTO.  # noqa: E501
        :rtype: UInt64DTO
        """
        return self._deadline

    @deadline.setter
    def deadline(self, deadline):
        """Sets the deadline of this TransactionStatusDTO.


        :param deadline: The deadline of this TransactionStatusDTO.  # noqa: E501
        :type: UInt64DTO
        """

        self._deadline = deadline

    @property
    def height(self):
        """Gets the height of this TransactionStatusDTO.  # noqa: E501


        :return: The height of this TransactionStatusDTO.  # noqa: E501
        :rtype: UInt64DTO
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this TransactionStatusDTO.


        :param height: The height of this TransactionStatusDTO.  # noqa: E501
        :type: UInt64DTO
        """

        self._height = height

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
        if issubclass(TransactionStatusDTO, dict):
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
        if not isinstance(other, TransactionStatusDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
