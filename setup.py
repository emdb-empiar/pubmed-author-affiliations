from setuptools import setup, find_packages
from os import listdir
from os.path import join

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='pubmed-author-affiliation',
    version='0.3',
    packages=find_packages(),
    data_files=[('example_input_data', [join('example_input_data', x) for x in listdir('example_input_data')])],
    url='https://github.com/emdb-empiar/pubmed-author-affiliations',
    license='Apache 2',
    author='Ardan Patwardhan',
    author_email='ardan@ebi.ac.uk',
    description='Search for author affiliations from Pubmed for a list of Pubmed IDs and DOIs',
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
