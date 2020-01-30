<p align="center"><a href="https://golang.org" target="_blank" rel="noopener noreferrer"><img width="300" src="https://github.com/proximax-storage/python-xpx-chain-sdk/raw/master/doc/ProximaX%20-%20Sirius%20Chain%20-%20Python%20-%20SDK.png" alt="Python logo"></a></p>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# ProximaX Sirius Blockchain Python SDK
Official ProximaX Sirius Blockchain SDK Library in Python.

The ProximaX Sirius Blockchain Python SDK is a Python library for interacting with the Sirius Blockchain.

## Getting Started
Clone the repository and build the SDK.
```bash
git clone git@github.com:proximax-storage/python-xpx-chain-sdk.git
cd python-xpx-chain-sdk/
python setup.py install
```
You can now start using the SDK modules.

## Example
```python
from xpxchain import client

# Get the current chain height of the Sirius test net
with client.BlockchainHTTP('bctestnet1.brimstone.xpxsirius.io:3000') as http:
    reply = http.get_blockchain_height()
    
print(reply)
```
For further examples please refer to [examples](examples/) directory or [E2E tests](tests/internet/)

##### ed25519 Secrets Warning
`SecretsWarning: Security warning: signing message using insecure ed25519 implementation, secrets may be leaked.`

SDK includes fallback ed25519 implementation in python when C implementation is not present. Python ed25519 implementation may lead to the disclosure of the secrets due to python's arbitrary-precision integer arithmetic. To get ed25519 C implementation please refer to https://pypi.org/project/ed25519sha3/

## Optimization

The SDK makes copious use of assertions to ensure functionality is correct during debugging, and during use of the client, it may be preferable to disable these assertions. This may be done by either setting the environment variable `PYTHONOPTIMIZE=TRUE`, or through the command-line flag `-O`.

In addition, installing [uvloop](https://github.com/magicstack/uvloop) may further improve asynchronous code performance.

## Testing

The SDK uses numerous tools to ensure type correctness, robust testing, and style conventions are preserved over multiple configurations. Before submitting any contributions, please resolve any issues that result from the following commands before committing:

```bash
# Run tox, which invokes numerous virtual envs to validate all configurations
# Invokes the unittest suite.
# Invokes the randomly-generated unittest suite.
# Invokes the linters, flake8 and pylint.
# Invokes bandit, a which checks for possible security risks.
# Invokes the type-checker, mypy.
# Invokes the complexity and maintainability checker, radon.
# Invokes the code coverage generator, coverage.
# Invokes the documentation builder, Sphinx.
$ tox
```

## Contributing

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in lexical by you, as defined in the Apache-2.0 license, shall be licensed as above, without any additional terms or conditions.
