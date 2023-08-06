from setuptools import setup, find_packages
from setuptools.command.install import install

import os
import sys

# This casues circular dependency problem on some systems (see: b2b089b8277fd6be411047fa8e7c512a57c21140)
# But works on others...
#from clusterone.version import VERSION

sys.path.append(os.path.join(os.path.dirname(__file__), "clusterone"))
from version import VERSION


setup(
    name='clusterone',
    version=VERSION,
    py_modules=[
        'clusterone'
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=[
        'click', 'py', 'coreapi-cli==1.0.6', 'gitpython', 'raven', 'terminaltables',
        'click_log==0.1.8', 'virtualenv', 'six',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-mock',
        ]
    },
    entry_points='''
        [console_scripts]
        just=clusterone.clusterone_cli:main
    ''',

    author="Clusterone",
    author_email="info@clusterone.com",
    description="Clusterone CLI and Python library.",
    license="MIT",
    keywords="",
    url="https://clusterone.com",
)
