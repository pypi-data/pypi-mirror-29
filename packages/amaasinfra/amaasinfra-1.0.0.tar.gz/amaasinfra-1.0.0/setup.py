"""AMaaS Infra."""
from setuptools import setup, find_packages


setup(
    name='amaasinfra',
    keywords=['amaas', 'infra', 'aws'],
    description='This is an essential package for managing AMaaS infra layer.',
    license='Apache License 2.0',
    install_requires=[
        'aws-requests-auth',
        'boto3',
        'configparser',
        'elasticsearch-dsl',
        'pyjwt',
        'pymysql',
        'requests',
    ],
    version='1.0.0',
    author='AMaaS Pte Ltd',
    author_email='tech@argomi.com',
    packages=find_packages(),
    platforms='any',
)
