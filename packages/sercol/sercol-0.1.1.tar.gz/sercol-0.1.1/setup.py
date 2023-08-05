# Copyright (c) 2014-2018. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import os
import re

from setuptools import setup

current_directory = os.path.dirname(__file__)
readme_filename = 'README.md'
readme_path = os.path.join(current_directory, readme_filename)

readme = ""
try:
    with open(readme_path, 'r') as f:
        readme = f.read()
except IOError as e:
    print(e)
    print("Failed to open %s" % readme_path)

try:
    import pypandoc
    readme = pypandoc.convert(readme, to='rst', format='md')
except ImportError as e:
    print(e)
    print("Failed to convert %s to reStructuredText", readme_filename)
    pass

with open('sercol/__init__.py', 'r') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read(),
        re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

if __name__ == '__main__':
    setup(
        name='sercol',
        version=version,
        description="Rich collection class with grouping and filtering helpers",
        author="Alex Rubinsteyn",
        author_email="alex.rubinsteyn@mssm.edu",
        url="https://github.com/openvax/sercol",
        license="http://www.apache.org/licenses/LICENSE-2.0.html",
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Operating System :: OS Independent',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
        ],
        install_requires=[
            "simplejson",
            "serializable",
            "pandas",
        ],
        long_description=readme,
        packages=['sercol'],
    )
