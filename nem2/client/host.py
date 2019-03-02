"""
    host
    ====

    HTTP client wrapper to inject the proper host (schema, domain and port)
    into requests providing solely a relative path.
"""

class Host:
    """Host wrapper for an abstract HTTP session."""

    def __init__(self, session, endpoint):
        """
        :param session: Requests or aiohttp-like HTTP client session.
        :param endpoint: Domain name and port for the endpoint.
        """
        self.session = session
        self.endpoint = endpoint

    def __enter__(self):
        return self

    def __exit__(self):
        self.session.close()

    def get(self, relative_path, *args, **kwds):
        """
        Make GET request from relative path.

        :param relative_path: Relative path from host prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self.endpoint + relative_path
        return self.session.get(path, *args, **kwds)

    def head(self, relative_path, *args, **kwds):
        """
        Make HEAD request from relative path.

        :param relative_path: Relative path from host prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self.endpoint + relative_path
        return self.session.head(path, *args, **kwds)

    def options(self, relative_path, *args, **kwds):
        """
        Make OPTIONS request from relative path.

        :param relative_path: Relative path from host prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self.endpoint + relative_path
        return self.session.options(path, *args, **kwds)

    def patch(self, relative_path, *args, **kwds):
        """
        Make PATCH request from relative path.

        :param relative_path: Relative path from host prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self.endpoint + relative_path
        return self.session.patch(path, *args, **kwds)

    def post(self, relative_path, *args, **kwds):
        """
        Make POST request from relative path.

        :param relative_path: Relative path from host prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self.endpoint + relative_path
        return self.session.post(path, *args, **kwds)

    def put(self, relative_path, *args, **kwds):
        """
        Make PUT request from relative path.

        :param relative_path: Relative path from host prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self.endpoint + relative_path
        return self.session.put(path, *args, **kwds)

    def delete(self, relative_path, *args, **kwds):
        """
        Make DELETE request from relative path.

        :param relative_path: Relative path from host prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self.endpoint + relative_path
        return self.session.delete(path, *args, **kwds)
