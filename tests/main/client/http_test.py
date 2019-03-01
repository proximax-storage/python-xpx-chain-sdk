import requests

from nem2 import client
from tests.harness import TestCase
from tests import responses


class HttpTest(TestCase):

    def test_exceptions(self):
        http = client.Http(responses.ENDPOINT)

        with self.assertRaises(requests.HTTPError):
            with requests.default_exception(requests.HTTPError):
                http.heartbeat()
        with self.assertRaises(ConnectionRefusedError):
            with requests.default_exception(ConnectionRefusedError):
                http.heartbeat()

    def test_heartbeat(self):
        http = client.Http(responses.ENDPOINT)

        with requests.default_response(200, **responses.HEARTBEAT["Ok"]):
            self.assertEqual(http.heartbeat(), client.Heartbeat.OK)

    def test_status(self):
        http = client.Http(responses.ENDPOINT)

        with requests.default_response(200, **responses.STATUS["Local"]):
            self.assertEqual(http.status(), client.Status.LOCAL)
        with requests.default_response(200, **responses.STATUS["Synchronized"]):
            self.assertEqual(http.status(), client.Status.SYNCHRONIZED)
        with requests.default_response(200, **responses.STATUS["Unknown"]):
            self.assertEqual(http.status(), client.Status.UNKNOWN)
        with self.assertRaises(ValueError):
            with requests.default_response(200, **responses.STATUS["Error"]):
                http.status()
