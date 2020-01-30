from xpxchain import models
from tests import harness

BLOCK_VALIDATOR = [
    lambda x: (x.channel_name, 'block'),
    lambda x: (isinstance(x.message, models.BlockInfo), True),
    lambda x: (x.message.height >= 1, True),
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
