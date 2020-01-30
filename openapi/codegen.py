"""
    codegen
    =======

    Automate swagger codegen for xpxchain/infrastructure.

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


MAVEN_HOST = 'http://central.maven.org'
MAVEN_CLI = MAVEN_HOST + '/maven2/org/openapitools/openapi-generator-cli'
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

        url = MAVEN_CLI + f'/{version}/openapi-generator-cli-{version}.jar'
        response = requests.get(url)
        response.raise_for_status()

        return response.content

    def write_file(version, content):
        """Write swagger codegen to file."""

        path = os.path.expanduser(f'~/bin/openapi-generator-cli-{version}.jar')
        with open(path, 'wb') as f:
            f.write(content)

    def write_symlink(version):
        """Generate a symlink to openapi-generator-cli."""

        src = os.path.expanduser(f'~/bin/openapi-generator-cli-{version}.jar')
        dst = os.path.expanduser('~/bin/openapi-generator-cli.jar')
        os.symlink(src, dst)

    if not which('openapi-generator-cli.jar'):
        version = parse_latest_version()
        content = get_swagger_codegen(version)
        write_file(version, content)
        write_symlink(version)


OPENAPI_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(OPENAPI_DIR)
NEM2_DIR = os.path.join(PROJECT_DIR, 'xpxchain')

def generate_infrastructure():
    """Run openapi-generator-cli to generate the Python code for infrastructure."""

    if not which('java'):
        raise ValueError('Cannot find system JAVA.')

    args = [
        'java', '-jar', which('openapi-generator-cli.jar'), 'generate',
        '--input-spec', f'{OPENAPI_DIR}/swagger.yaml',
        '--generator-name', 'python-aiohttp',
        '--output', f'{OPENAPI_DIR}/codegen',
        '--package-name', 'infrastructure',
        #'--library'
    ]
    subprocess.run(args, check=True, capture_output=False)


def patch_infrastructure():
    """
    Patch the absolute imports to use relative imports.

    This tracks the current depth of the submodule relative to the Swagger
    infrastructure module depth, and converts all absolute imports into
    relative imports. This is relatively hacky, and ideally should be improved
    before being used in production.
    """

    def read_file(path):
        """Read file from full-path."""

        with open(path, 'r') as f:
            return f.read().splitlines()

    def write_file(path, lines):
        """Write file to full-path."""

        with open(path, 'w') as f:
            return f.write(os.linesep.join(lines))

    def remove_use_absolute_import(lines):
        """Remove the `from __future__ import absolute_import` directive."""

        for i, line in enumerate(lines):
            if line.startswith('from __future__ import absolute_import'):
                # Delete the line and the subsequent empty line.
                del lines[i:i+2]
                break

    def remove_absolute_imports(lines, module, depth):
        """Patch any lines using absolute imports."""

        def condition(item, keyword):
            return item.startswith(keyword) and 'infrastructure' in item

        def filter_lines(keyword):
            return (i for i in enumerate(lines) if condition(i[1], keyword))

        froms = filter_lines('from')
        imports = filter_lines('import')
        periods = '.' * depth

        # Patch froms
        from_module_dot = f'from {module}.'
        from_module = f'from {module} '
        from_infra_dot = f'from infrastructure.'
        from_infra = f'from infrastructure '
        for index, line in froms:
            if from_module_dot in line:
                # Have a trailing period after the full qualified module, can
                # just remove {module}.
                lines[index] = line.replace(from_module_dot, 'from .')
            elif from_module in line:
                # No trailing period, replace `from {module}` with `from .`
                lines[index] = line.replace(from_module, 'from .')
            elif from_infra_dot in line:
                # Starts with a different prefix, replace it with the depth.
                lines[index] = line.replace(from_infra_dot, f'from {periods}')
            else:
                # No period, don't need to remove the period
                lines[index] = line.replace(from_infra, f'from {periods}')

        # Patch imports
        import_infra_dot = f'import infrastructure.'
        for index, line in imports:
            if import_infra_dot in line:
                newmod = line[len(import_infra_dot):]
                oldmod = f'infrastructure.{newmod}'
                lines[index] = line.replace(import_infra_dot, f'from {periods} import ')
                for i in range(index+1, len(lines)):
                    line = lines[i]
                    if not line.startswith(('from', 'import')):
                        lines[i] = line.replace(oldmod, newmod)
            else:
                # Importing the current root, error
                raise ValueError('Cannot import root.')

    def patch_file(root, path):
        """Patch a single file to use relative and not absolute imports."""

        full_path = os.path.join(root, path)

        # Need to get the module prefix
        dirname = os.path.dirname(path)
        modules = ['infrastructure']
        if dirname:
            modules += dirname.split(os.pathsep)
        module = '.'.join(modules)

        # Depth, or number of periods for anything else
        depth = len(modules)

        # Patch the file
        lines = read_file(full_path)
        remove_use_absolute_import(lines)
        remove_absolute_imports(lines, module, depth)
        write_file(full_path, lines)

    infrastructure = os.path.join(OPENAPI_DIR, 'codegen', 'infrastructure')
    for root, _, files in os.walk(infrastructure):
        for name in files:
            path = os.path.join(root, name)
            relpath = os.path.relpath(path, infrastructure)
            patch_file(infrastructure, relpath)


def replace_infrastructure():
    """Replace the generated infrastructure."""

    dst = os.path.join(NEM2_DIR, 'infrastructure')
    codegen = os.path.join(OPENAPI_DIR, 'codegen')
    src = os.path.join(codegen, 'infrastructure')

    # Remove the old, existing xpxchain infrastructure folder.
    shutil.rmtree(dst, ignore_errors=True)

    # Move the swagger client to the infrastructure folder.
    shutil.move(src, dst)

    # Remove the remaining generated code.
    shutil.rmtree(codegen, ignore_errors=True)


if __name__ == '__main__':
    fetch_swagger_codegen()
    generate_infrastructure()
    patch_infrastructure()
    replace_infrastructure()
