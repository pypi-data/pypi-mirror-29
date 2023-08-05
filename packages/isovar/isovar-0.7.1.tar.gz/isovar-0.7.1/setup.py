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

from __future__ import (absolute_import,)

import os
import logging
import re

from setuptools import setup, find_packages

readme_dir = os.path.dirname(__file__)
readme_path = os.path.join(readme_dir, 'README.md')

try:
    with open(readme_path, 'r') as f:
        readme_markdown = f.read()
except:
    logging.warn("Failed to load %s" % readme_path)
    readme_markdown = ""

try:
    import pypandoc
    readme_restructured = pypandoc.convert(readme_markdown, to='rst', format='md')
    with open(readme_path.replace(".md", ".rst"), "w") as f:
        f.write(readme_restructured)
except:
    logging.warn("Conversion of long_description from MD to RST failed")
    pass


with open('isovar/__init__.py', 'r') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read(),
        re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

if __name__ == '__main__':
    setup(
        name='isovar',
        version=version,
        description="Assemble transcript sequences fragments near variants",
        author="Alex Rubinsteyn and Arman Aksoy",
        author_email="alex.rubinsteyn@mssm.edu",
        url="https://github.com/hammerlab/isovar",
        license="http://www.apache.org/licenses/LICENSE-2.0.html",
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Operating System :: OS Independent',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
        ],
        install_requires=[
            'six',
            'pysam >= 0.9.0',
            'pandas',
            'varcode>=0.5.9',
            'pyensembl>=1.0.3',
        ],
        long_description=readme_restructured,
        packages=find_packages(),
        package_data={'isovar.cli': ['logging.conf']},
        scripts=[
            "script/isovar-protein-sequences.py",
            "script/isovar-translations.py",
            "script/isovar-reference-contexts.py",
            "script/isovar-allele-reads.py",
            "script/isovar-allele-counts.py",
            "script/isovar-variant-reads.py",
            "script/isovar-variant-sequences.py",
        ],
    )
