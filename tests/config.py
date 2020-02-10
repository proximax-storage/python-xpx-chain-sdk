
from xpxchain import models
import json

# Generation hash can be found in the first block of a chain
# /block/1
gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'

# Main mosaic can be found in the receipt of the second block
# /block/2/receipts
# We use hex representation of high 4 bytes + low 4 bytes
mosaic_data = json.loads('{"mosaicId":[481110499,231112638]}')
hex_id = "%08x%08x" % (mosaic_data['mosaicId'][1], mosaic_data['mosaicId'][0])
mosaic_id = models.MosaicId.create_from_hex(hex_id)

# Folowing keys must be given to you
nemesis_harvesting_public_key = '346E56F77F07B19D48B3AEF969EDB01F68A5AC9FAF8E5E007577D71BA66385FB'
api_node_public_key = '460458B98E2BAA36A8E95DE9B320379E89898885B71CF0174E02F1324FAFFAC1'
nemesis = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
nemesis_signer = models.Account.create_from_private_key('C06B2CC5D7B66900B2493CF68BE10B7AA8690D973B7F0B65D0DAE4F7AA464716', models.NetworkType.MIJIN_TEST)
