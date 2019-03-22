from nem2 import client
from nem2 import models
from tests import harness
from tests import responses

BLOCK_VALIDATOR = [
    lambda x: (x.channel_name, 'block'),
    lambda x: (isinstance(x.message, models.BlockInfo), True),
    lambda x: (x.message.height >= 23230, True),
]


@harness.listener_test_case({
    'tests': [
        {
            'name': 'test_new_block',
            'subscriptions': ['new_block'],
            'validation': [BLOCK_VALIDATOR],
        },
    ],
})
class TestListener(harness.TestCase):
    pass
