from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PubMedResultClustering',
    version='1.0',
    url='https://github.com/aparnathinks/PubMedResultClustering',
    author='Aparna Subramanian',
    author_email='aparnas1@umbc.edu',
    description='Cluster pubmed articles to prepare them for search'
)

