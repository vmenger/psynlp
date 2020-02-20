# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
# from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

version = {}
with open(path.join(here, 'psynlp', '__version__.py')) as fp:
    exec(fp.read(), version)

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='psynlp',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version['__version__'],

    description="psynlp: a collection of NLP functionality for analyzing psychiatric clinical text",

    # The project's main homepage.
    url='https://github.com/vmenger/psynlp',

    # Author details
    author='Vincent Menger',
    author_email='v.menger@umcutrecht.nl',

    packages=find_packages(),

    # Data files
    include_package_data=True,

    # Choose your license
    license='GNU GPLv3',

    # What does your project relate to?
    keywords=['psychiatry', 'nlp', 'clinical text'],

    install_requires=[
                    'doublemetaphone',
                    'gensim', 
                    'nltk', 
                    'pandas', 
                    'psydata',
                    'spacy', 
                    ],
)