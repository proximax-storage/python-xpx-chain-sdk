"""
    codegen
    =======

    Automate swagger codegen for nem2/infrastructure.

    License
    -------

    Copyright 2019 NEM

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import os
import re
import requests
import shutil
import subprocess
import xml.etree.cElementTree as ET


def which(name):
    """
    Analogous to UNIX which command.

    Find the first element with the name in the path.

    :name: Filename of an executable.
    """

    for directory in os.getenv("PATH").split(os.path.pathsep):
        path = directory + os.sep + name
        if os.path.exists(path):
            return path

    raise ValueError('Unable to find given path.')


MAVEN_HOST = 'https://repo1.maven.org'
MAVEN_CLI = MAVEN_HOST + '/maven2/io/swagger/swagger-codegen-cli'
SEMVERSION = re.compile(r'\A\d+\.\d+\.\d+\Z')

def fetch_swagger_codegen():
    """Fetch the latest version of swagger codegen."""

    def get_latest_version():
        """Get the latest version of swagger codegen."""

        url = MAVEN_CLI + '/maven-metadata.xml'
        response = requests.get(url)
        response.raise_for_status()

        return response.content

    def parse_latest_version():
        """Parse the latest version of swagger codegen."""

        xml = get_latest_version()
        root = ET.fromstring(xml)
        versions_node = root.find('versioning').find('versions')
        versions = list(versions_node.iter('version'))
        for version_node in reversed(versions):
            # Skip release candidate versions. Just use latest stable branch.
            if SEMVERSION.match(version_node.text):
                return version_node.text
        raise ValueError('Unable to find suitable stable version.')

    def get_swagger_codegen(version):
        """Get the latest swagger codegen jar."""

        url = MAVEN_CLI + f'/{version}/swagger-codegen-cli-{version}.jar'
        response = requests.get(url)
        response.raise_for_status()

        return response.content

    def write_file(version, content):
        """Write swagger codegen to file."""

        path = os.path.expanduser(f'~/bin/swagger-codegen-cli-{version}.jar')
        with open(path, 'wb') as f:
            f.write(content)

    def write_symlink(version):
        """Generate a symlink to swagger-codegen-cli."""

        src = os.path.expanduser(f'~/bin/swagger-codegen-cli-{version}.jar')
        dst = os.path.expanduser('~/bin/swagger-codegen-cli.jar')
        os.symlink(src, dst)

    if not which('swagger-codegen-cli.jar'):
        version = parse_latest_version()
        content = get_swagger_codegen(version)
        write_file(version, content)
        write_symlink(version)


SWAGGER_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(SWAGGER_DIR)
NEM2_DIR = os.path.join(PROJECT_DIR, 'nem2')

def generate_infrastructure():
    """Run swagger-codegen-cli to generate the Python code for infrastructure."""

    if not which('java'):
        raise ValueError('Cannot find system JAVA.')

    args = [
        'java', '-jar', which('swagger-codegen-cli.jar'), 'generate',
        '--input-spec', f'{SWAGGER_DIR}/swagger.yaml',
        '--lang', 'python',
        '--output', f'{SWAGGER_DIR}/codegen',
    ]
    subprocess.run(args, check=True, capture_output=True)


def replace_infrastructure():
    """Replace the generated infrastructure."""

    infrastructure = f'{NEM2_DIR}/infrastructure'
    codegen = os.path.join(SWAGGER_DIR, 'codegen')
    swagger_client = os.path.join(codegen, 'swagger_client')

    # Remove the old, existing nem2 infrastructure folder.
    shutil.rmtree(infrastructure, ignore_errors=True)

    # Move the swagger client to the infrastructure folder.
    shutil.move(swagger_client, infrastructure)

    # Remove the remaining generated code.
    shutil.rmtree(codegen, ignore_errors=True)


if __name__ == '__main__':
    fetch_swagger_codegen()
    generate_infrastructure()
    replace_infrastructure()
