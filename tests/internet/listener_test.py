from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestListener(harness.TestCase):

    async def test_block(self):
        async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
            await listener.new_block()
            async for message in listener:
                self.assertEqual(message.channel_name, 'block')
                self.assertIsInstance(message.message, models.BlockInfo)
                self.assertGreaterEqual(message.message.height, 23230)
                break
