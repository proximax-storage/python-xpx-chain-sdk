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
            subprocess.call(command, **kwds)

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
MAINTAINER = ['Alex Huszagh']
MAINTAINER_EMAIL = ['ahuszagh@gmail.com']
NAME = "nem2"
URL = "https://github.com/nemtech/nem2-sdk-python.git"
VERSION = "0.0.1"

DESCRIPTION = "Python SDK for NEM2."
LONG_DESCRIPTION = "TODO(ahuszagh) Implement..."

PACKAGES = setuptools.find_packages()

REQUIRES = [
    'aiohttp>=3.5',
    'requests>=2.21',
    'websockets>=7.0',
]

TESTS_REQUIRE = [
    'pycryptodome>=3.4',
]

EXTRAS_REQUIRE = {
    'sphinx': ['sphinx_rtd_theme>=0.4', 'sphinx_autodoc_typehints'],
    'crypto': ['pycryptodome>=3.4', 'ed25519>=1.4', 'ed25519sha3>=1.4'],
    'reactive': ['rx>=1.6'],
}

# Define endpoint for internet tests in a single place.
ENDPOINT = "localhost:3000"
# Inject a mockdir to inject custom HTTP clients.
PROJECTDIR = os.path.dirname(os.path.realpath(__file__))
MOCKDIR = os.path.join(PROJECTDIR, 'mock')
COMMANDS = {
    'doc': shell_command(
        command=[sys.executable, "setup.py", "build_sphinx"],
        short_description="Build project documentation.",
        PYTHONPATH=MOCKDIR
    ),
    'mypy': shell_command(
        command=[sys.executable, "-m", "mypy", "nem2"],
        short_description="Run mypy on project.",
    ),
    'lint': shell_command(
        command=[sys.executable, "-m", "flake8"],
        short_description="Run flake8 on project.",
    ),
    'lint_tests': shell_command(
        command=[sys.executable, "-m", "flake8", "tests"],
        short_description="Run flake8 on unit tests.",
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
)
