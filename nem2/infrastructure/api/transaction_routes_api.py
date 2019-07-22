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


class TransactionRoutesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def announce_cosignature_transaction(self, payload, **kwargs):  # noqa: E501
        """Announce a cosignature transaction  # noqa: E501

        Announces a [cosignature transaction](https://nemtech.github.io/concepts/aggregate-transaction.html#cosignature-transaction) to the network.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announce_cosignature_transaction(payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransactionPayload payload: The transaction [payload](https://nemtech.github.io/api.html#serialization). (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.announce_cosignature_transaction_with_http_info(payload, **kwargs)  # noqa: E501
        else:
            (data) = self.announce_cosignature_transaction_with_http_info(payload, **kwargs)  # noqa: E501
            return data

    def announce_cosignature_transaction_with_http_info(self, payload, **kwargs):  # noqa: E501
        """Announce a cosignature transaction  # noqa: E501

        Announces a [cosignature transaction](https://nemtech.github.io/concepts/aggregate-transaction.html#cosignature-transaction) to the network.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announce_cosignature_transaction_with_http_info(payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransactionPayload payload: The transaction [payload](https://nemtech.github.io/api.html#serialization). (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['payload']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method announce_cosignature_transaction" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'payload' is set
        if ('payload' not in params or
                params['payload'] is None):
            raise ValueError("Missing the required parameter `payload` when calling `announce_cosignature_transaction`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'payload' in params:
            body_params = params['payload']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/transaction/cosignature', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def announce_partial_transaction(self, payload, **kwargs):  # noqa: E501
        """Announce an aggregate bonded transaction  # noqa: E501

        Announces an [aggregate bonded transaction](https://nemtech.github.io/concepts/aggregate-transaction.html#aggregate-bonded) to the network.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announce_partial_transaction(payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransactionPayload payload: The transaction [payload](https://nemtech.github.io/api.html#serialization). (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.announce_partial_transaction_with_http_info(payload, **kwargs)  # noqa: E501
        else:
            (data) = self.announce_partial_transaction_with_http_info(payload, **kwargs)  # noqa: E501
            return data

    def announce_partial_transaction_with_http_info(self, payload, **kwargs):  # noqa: E501
        """Announce an aggregate bonded transaction  # noqa: E501

        Announces an [aggregate bonded transaction](https://nemtech.github.io/concepts/aggregate-transaction.html#aggregate-bonded) to the network.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announce_partial_transaction_with_http_info(payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransactionPayload payload: The transaction [payload](https://nemtech.github.io/api.html#serialization). (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['payload']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method announce_partial_transaction" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'payload' is set
        if ('payload' not in params or
                params['payload'] is None):
            raise ValueError("Missing the required parameter `payload` when calling `announce_partial_transaction`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'payload' in params:
            body_params = params['payload']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/transaction/partial', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def announce_transaction(self, payload, **kwargs):  # noqa: E501
        """Announce a new transaction  # noqa: E501

        Announces a transaction to the network. It is recommended to use the NEM2-SDK to announce transactions as they should be [serialized](https://nemtech.github.io/api.html#serialization).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announce_transaction(payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransactionPayload payload: The transaction [payload](https://nemtech.github.io/api.html#serialization). (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.announce_transaction_with_http_info(payload, **kwargs)  # noqa: E501
        else:
            (data) = self.announce_transaction_with_http_info(payload, **kwargs)  # noqa: E501
            return data

    def announce_transaction_with_http_info(self, payload, **kwargs):  # noqa: E501
        """Announce a new transaction  # noqa: E501

        Announces a transaction to the network. It is recommended to use the NEM2-SDK to announce transactions as they should be [serialized](https://nemtech.github.io/api.html#serialization).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announce_transaction_with_http_info(payload, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransactionPayload payload: The transaction [payload](https://nemtech.github.io/api.html#serialization). (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['payload']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method announce_transaction" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'payload' is set
        if ('payload' not in params or
                params['payload'] is None):
            raise ValueError("Missing the required parameter `payload` when calling `announce_transaction`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'payload' in params:
            body_params = params['payload']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/transaction', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_transaction(self, transaction_id, **kwargs):  # noqa: E501
        """Get transaction information  # noqa: E501

        Returns transaction information given a transactionId or hash.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_transaction(transaction_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str transaction_id: The transaction id or hash. (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_transaction_with_http_info(transaction_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_transaction_with_http_info(transaction_id, **kwargs)  # noqa: E501
            return data

    def get_transaction_with_http_info(self, transaction_id, **kwargs):  # noqa: E501
        """Get transaction information  # noqa: E501

        Returns transaction information given a transactionId or hash.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_transaction_with_http_info(transaction_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str transaction_id: The transaction id or hash. (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['transaction_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_transaction" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'transaction_id' is set
        if ('transaction_id' not in params or
                params['transaction_id'] is None):
            raise ValueError("Missing the required parameter `transaction_id` when calling `get_transaction`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'transaction_id' in params:
            path_params['transactionId'] = params['transaction_id']  # noqa: E501

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
            '/transaction/{transactionId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_transaction_status(self, hash, **kwargs):  # noqa: E501
        """Get transaction status  # noqa: E501

        Returns the transaction status for a given hash.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_transaction_status(hash, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str hash: The transaction hash. (required)
        :return: TransactionStatusDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_transaction_status_with_http_info(hash, **kwargs)  # noqa: E501
        else:
            (data) = self.get_transaction_status_with_http_info(hash, **kwargs)  # noqa: E501
            return data

    def get_transaction_status_with_http_info(self, hash, **kwargs):  # noqa: E501
        """Get transaction status  # noqa: E501

        Returns the transaction status for a given hash.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_transaction_status_with_http_info(hash, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str hash: The transaction hash. (required)
        :return: TransactionStatusDTO
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['hash']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_transaction_status" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'hash' is set
        if ('hash' not in params or
                params['hash'] is None):
            raise ValueError("Missing the required parameter `hash` when calling `get_transaction_status`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'hash' in params:
            path_params['hash'] = params['hash']  # noqa: E501

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
            '/transaction/{hash}/status', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionStatusDTO',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_transactions(self, transaction_ids, **kwargs):  # noqa: E501
        """Get transactions information  # noqa: E501

        Returns transactions information for a given array of transactionIds.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_transactions(transaction_ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransactionIds transaction_ids: An array of transaction ids or hashes. (required)
        :return: list[object]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_transactions_with_http_info(transaction_ids, **kwargs)  # noqa: E501
        else:
            (data) = self.get_transactions_with_http_info(transaction_ids, **kwargs)  # noqa: E501
            return data

    def get_transactions_with_http_info(self, transaction_ids, **kwargs):  # noqa: E501
        """Get transactions information  # noqa: E501

        Returns transactions information for a given array of transactionIds.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_transactions_with_http_info(transaction_ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransactionIds transaction_ids: An array of transaction ids or hashes. (required)
        :return: list[object]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['transaction_ids']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_transactions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'transaction_ids' is set
        if ('transaction_ids' not in params or
                params['transaction_ids'] is None):
            raise ValueError("Missing the required parameter `transaction_ids` when calling `get_transactions`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'transaction_ids' in params:
            body_params = params['transaction_ids']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/transaction', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[object]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_transactions_statuses(self, transaction_hashes, **kwargs):  # noqa: E501
        """Get transactions status.  # noqa: E501

        Returns an array of transaction statuses for a given array of transaction hashes.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_transactions_statuses(transaction_hashes, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransactionHashes transaction_hashes: An array of transaction hashes. (required)
        :return: list[TransactionStatusDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_transactions_statuses_with_http_info(transaction_hashes, **kwargs)  # noqa: E501
        else:
            (data) = self.get_transactions_statuses_with_http_info(transaction_hashes, **kwargs)  # noqa: E501
            return data

    def get_transactions_statuses_with_http_info(self, transaction_hashes, **kwargs):  # noqa: E501
        """Get transactions status.  # noqa: E501

        Returns an array of transaction statuses for a given array of transaction hashes.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_transactions_statuses_with_http_info(transaction_hashes, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TransactionHashes transaction_hashes: An array of transaction hashes. (required)
        :return: list[TransactionStatusDTO]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['transaction_hashes']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_transactions_statuses" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'transaction_hashes' is set
        if ('transaction_hashes' not in params or
                params['transaction_hashes'] is None):
            raise ValueError("Missing the required parameter `transaction_hashes` when calling `get_transactions_statuses`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'transaction_hashes' in params:
            body_params = params['transaction_hashes']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/transaction/statuses', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[TransactionStatusDTO]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
