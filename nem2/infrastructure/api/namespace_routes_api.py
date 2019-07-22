# coding: utf-8

"""
    Catapult REST API Reference

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.12
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from swagger_client.api_client import ApiClient


class NamespaceRoutesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_namespace(self, namespace_id, **kwargs):  # noqa: E501
        """Get namespace information  # noqa: E501

        Gets the namespace for a given namespaceId.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_namespace(namespace_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str namespace_id: The namespace identifier. (required)
        :return: NamespaceInfoDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_namespace_with_http_info(namespace_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_namespace_with_http_info(namespace_id, **kwargs)  # noqa: E501
            return data

    def get_namespace_with_http_info(self, namespace_id, **kwargs):  # noqa: E501
        """Get namespace information  # noqa: E501

        Gets the namespace for a given namespaceId.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_namespace_with_http_info(namespace_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str namespace_id: The namespace identifier. (required)
        :return: NamespaceInfoDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['namespace_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_namespace" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'namespace_id' is set
        if ('namespace_id' not in params or
                params['namespace_id'] is None):
            raise ValueError("Missing the required parameter `namespace_id` when calling `get_namespace`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'namespace_id' in params:
            path_params['namespaceId'] = params['namespace_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/namespace/{namespaceId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NamespaceInfoDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_namespaces_from_account(self, account_id, **kwargs):  # noqa: E501
        """Get namespaces owned by an account  # noqa: E501

        Gets an array of namespaces for a given account address.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_namespaces_from_account(account_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: The address or public key of the account. (required)
        :param int page_size: The number of namespaces to return.
        :param str id: The namespace id up to which namespace objects are returned.
        :return: list[NamespaceInfoDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_namespaces_from_account_with_http_info(account_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_namespaces_from_account_with_http_info(account_id, **kwargs)  # noqa: E501
            return data

    def get_namespaces_from_account_with_http_info(self, account_id, **kwargs):  # noqa: E501
        """Get namespaces owned by an account  # noqa: E501

        Gets an array of namespaces for a given account address.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_namespaces_from_account_with_http_info(account_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str account_id: The address or public key of the account. (required)
        :param int page_size: The number of namespaces to return.
        :param str id: The namespace id up to which namespace objects are returned.
        :return: list[NamespaceInfoDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account_id', 'page_size', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_namespaces_from_account" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `get_namespaces_from_account`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'account_id' in params:
            path_params['accountId'] = params['account_id']  # noqa: E501

        query_params = []
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'id' in params:
            query_params.append(('id', params['id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/account/{accountId}/namespaces', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[NamespaceInfoDTO]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_namespaces_from_accounts(self, addresses, **kwargs):  # noqa: E501
        """Get namespaces for given array of addresses  # noqa: E501

        Gets namespaces for a given array of addresses.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_namespaces_from_accounts(addresses, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Addresses addresses: An array of addresses. (required)
        :param int page_size: The number of namespaces to return.
        :param str id: The namespace id up to which namespace objects are returned.
        :return: list[NamespaceInfoDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_namespaces_from_accounts_with_http_info(addresses, **kwargs)  # noqa: E501
        else:
            (data) = self.get_namespaces_from_accounts_with_http_info(addresses, **kwargs)  # noqa: E501
            return data

    def get_namespaces_from_accounts_with_http_info(self, addresses, **kwargs):  # noqa: E501
        """Get namespaces for given array of addresses  # noqa: E501

        Gets namespaces for a given array of addresses.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_namespaces_from_accounts_with_http_info(addresses, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Addresses addresses: An array of addresses. (required)
        :param int page_size: The number of namespaces to return.
        :param str id: The namespace id up to which namespace objects are returned.
        :return: list[NamespaceInfoDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['addresses', 'page_size', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_namespaces_from_accounts" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'addresses' is set
        if ('addresses' not in params or
                params['addresses'] is None):
            raise ValueError("Missing the required parameter `addresses` when calling `get_namespaces_from_accounts`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'id' in params:
            query_params.append(('id', params['id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'addresses' in params:
            body_params = params['addresses']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/account/namespaces', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[NamespaceInfoDTO]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_namespaces_names(self, namespace_ids, **kwargs):  # noqa: E501
        """Get readable names for a set of namespaces  # noqa: E501

        Returns friendly names for mosaics.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_namespaces_names(namespace_ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param NamespaceIds namespace_ids: An array of namespaceIds. (required)
        :return: list[NamespaceNameDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_namespaces_names_with_http_info(namespace_ids, **kwargs)  # noqa: E501
        else:
            (data) = self.get_namespaces_names_with_http_info(namespace_ids, **kwargs)  # noqa: E501
            return data

    def get_namespaces_names_with_http_info(self, namespace_ids, **kwargs):  # noqa: E501
        """Get readable names for a set of namespaces  # noqa: E501

        Returns friendly names for mosaics.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_namespaces_names_with_http_info(namespace_ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param NamespaceIds namespace_ids: An array of namespaceIds. (required)
        :return: list[NamespaceNameDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['namespace_ids']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_namespaces_names" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'namespace_ids' is set
        if ('namespace_ids' not in params or
                params['namespace_ids'] is None):
            raise ValueError("Missing the required parameter `namespace_ids` when calling `get_namespaces_names`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'namespace_ids' in params:
            body_params = params['namespace_ids']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/namespace/names', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[NamespaceNameDTO]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
