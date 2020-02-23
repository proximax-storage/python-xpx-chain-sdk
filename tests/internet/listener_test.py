from xpxchain import models
from xpxchain import client
from tests import harness
from tests import config

class TestListener(harness.TestCase):
    
    async def test_new_block(self):
        async with client.Listener(f'{config.ENDPOINT}/ws') as listener:
            await listener.new_block()

            async for m in listener:
                self.assertEqual(m.channel_name, 'block')
                self.assertEqual(isinstance(m.message, models.BlockInfo), True)
                self.assertEqual(m.message.height >= 1, True)
                break
