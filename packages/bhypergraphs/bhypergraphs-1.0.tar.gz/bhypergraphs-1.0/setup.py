
from setuptools import setup, find_packages

import bhg

setup(
    name='bhypergraphs',
    version=bhg.__version__,
    author=bhg.__author__,
    author_email=bhg.__email__,
    url='https://bitbucket.org/blins/hypergraphs',
    packages=find_packages(),
    install_requires=[
        'objects_query==1.0'
        ],
)