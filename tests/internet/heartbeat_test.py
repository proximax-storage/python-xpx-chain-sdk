# TODO(ahuszagh) Remove
#from nem2 import client
#from tests.harness import AsyncTestCase, TestCase
#from tests import responses
#
#
#class HeartbeatTest(TestCase):
#
#    def test_sync(self):
#        http = client.Http(responses.ENDPOINT)
#        self.assertEqual(http.heartbeat(), client.Heartbeat.OK)
#
#
#class AsyncHeartbeatTest(AsyncTestCase):
#
#    async def test_async(self):
#        http = client.AsyncHttp(responses.ENDPOINT)
#        self.assertEqual(await http.heartbeat(), client.Heartbeat.OK)
