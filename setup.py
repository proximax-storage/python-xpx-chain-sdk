import os
import setuptools
import subprocess
import sys


def shell_command(command, short_description, **env):
    """Create a simple command that is invoked using subprocess."""

    kwds = {}
    if env:
        environ = os.environ.copy()
        environ.update(env)
        kwds['env'] = environ

    class ShellCommand(setuptools.Command):
        """Run custom script when invoked."""

        description = short_description
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            subprocess.check_call(command, **kwds)

    return ShellCommand


def unittest_command(suite):
    """Get new command for unittest suite."""

    return [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-v",
        "-s",
        suite,
        "-p",
        "*_test.py"
    ]


LICENSE = "Apache-2.0"
MAINTAINER = "Jan"
MAINTAINER_EMAIL = "wirfeon@gmail.com"
NAME = "xpx-chain"
URL = "https://github.com/proximax-storage/python-xpx-chain-sdk"
VERSION = "0.6.5"

DESCRIPTION = "ProximaX Sirius Blockchain Python SDK"
LONG_DESCRIPTION = "ProximaX Sirius Blockchain Python SDK is a Python library for interacting with the Sirius Blockchain."

PACKAGES = setuptools.find_packages()

REQUIRES = [
    'aiohttp>=3.5,<4',
    'bidict>=0.18',
    'requests>=2.21',
    'websockets>=7.0',
    'ed25519sha3>=1.4.1',
]

TESTS_REQUIRE = [
    'pycryptodome>=3.4',
]

EXTRAS_REQUIRE = {
    # FEATURES

    # Use C-extensions for cryptographic libraries for performance and security.
    'crypto': ['pycryptodome>=3.4', 'ed25519>=1.4', 'ed25519sha3>=1.4'],
    # Use ReactiveX for asynchronous code scheduling.
    'reactive': ['rx>=1.6'],

    # TESTING / DOCUMENTATION

    # Use Bandit to detect potential code security risks.
    'bandit': ['bandit>=1.5'],
    # Determine and report code coverage from unittests.
    'coverage': ['flake8>=4.5', 'nose2>=0.9'],
    # Use PyFlake8 to lint code, detect logic errors, and check code complexity.
    'flake8': ['flake8>=3.7', 'mccabe>=0.6'],
    # Use Pylint to lint code and report code quality.
    'pylint': ['pylint>=2.3'],
    # Use rstr to generate random data for unit testing.
    'random': ['rstr>=2.2'],
    # Use radon to check code complexity and maintainability.
    'radon': ['radon>=3.0'],
    # Use Sphinx to build project documentation.
    'sphinx': ['sphinx_rtd_theme>=0.4', 'sphinx_autodoc_typehints'],
}

# Define endpoint for internet tests in a single place.
ENDPOINT = "//localhost:3000"
# Inject a mockdir to inject custom HTTP clients.
PROJECTDIR = os.path.dirname(os.path.realpath(__file__))
MOCKDIR = os.path.join(PROJECTDIR, 'mock')
COMMANDS = {
    'bandit': shell_command(
        command=[sys.executable, "-m", "bandit", "-r", "xpxchain", "-c", ".bandit.yml"],
        short_description="Run bandit on project.",
    ),
    'coverage': shell_command(
        command=[sys.executable, "-m", "nose2", "--config", ".nose2"],
        short_description="Run main unittest suite.",
        PYTHONPATH=MOCKDIR
    ),
    'doc': shell_command(
        command=[sys.executable, "setup.py", "build_sphinx"],
        short_description="Build project documentation.",
        PYTHONPATH=MOCKDIR
    ),
    'flake8': shell_command(
        command=[sys.executable, "-m", "flake8", "--max-complexity", "10", "--max-line-length", "120", "xpxchain"],
        short_description="Run flake8 on project.",
    ),
    'flake8_tests': shell_command(
        command=[sys.executable, "-m", "flake8", "tests"],
        short_description="Run flake8 on unit tests.",
    ),
    'mypy': shell_command(
        command=[sys.executable, "-m", "mypy", "xpxchain"],
        short_description="Run mypy on project.",
    ),
    'pylint': shell_command(
        command=[sys.executable, "-m", "pylint", "xpxchain"],
        short_description="Run pylint on project.",
    ),
    'radon_cc': shell_command(
        command=[sys.executable, "-m", "radon", "cc", "--min", "C", "xpxchain"],
        short_description="Run radon's code-complexity checker on project.",
    ),
    'radon_mi': shell_command(
        command=[sys.executable, "-m", "radon", "mi", "--min", "B", "xpxchain"],
        short_description="Run radon's maintainability index checker on project.",
    ),
    'random': shell_command(
        command=unittest_command("tests.random"),
        short_description="Run randomly-generated unittest suite.",
    ),
    'test': shell_command(
        command=unittest_command("tests.main"),
        short_description="Run main unittest suite.",
        PYTHONPATH=MOCKDIR
    ),
    'test_internet': shell_command(
        command=unittest_command("tests.internet"),
        short_description="Run internet-dependent unittest suite.",
        NIS2_ENDPOINT=ENDPOINT
    ),
}

setuptools.setup(
    install_requires=REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.7",
    tests_require=TESTS_REQUIRE,
    packages=PACKAGES,
    cmdclass=COMMANDS,
    zip_safe=False,
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=URL,
    license=LICENSE,
    keywords=['ProximaX', 'XPX', 'Sirius', 'Catapult', 'Blockchain'],
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ]
)
