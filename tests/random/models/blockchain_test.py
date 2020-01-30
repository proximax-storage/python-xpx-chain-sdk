from xpxchain import models
from tests import harness


class TestBlockchainScore(harness.TestCase):

    @harness.randomize
    def test_valid(self, score: harness.U128):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.BlockchainScore(score)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.BlockchainScore.create_from_dto(dto, network_type))

    @harness.randomize(score={'min_value': -1 << 32, 'max_value': -1})
    def test_invalid(self, score: int):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.BlockchainScore(score)
        with self.assertRaises(ArithmeticError):
            model.to_dto(network_type)
