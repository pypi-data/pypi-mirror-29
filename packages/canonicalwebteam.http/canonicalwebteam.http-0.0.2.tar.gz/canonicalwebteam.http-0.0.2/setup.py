from setuptools import setup

setup(
    name='canonicalwebteam.http',
    version='0.0.2',
    author='Canonical Webteam',
    url='https://github.com/canonical-webteam/http',
    packages=[
        'canonicalwebteam',
        'canonicalwebteam.http'
    ],
    description=(
        'Basic opinionated functions for making HTTP calls '
        'in Webteam python projects'
    ),
    install_requires=[
        "requests-cache >= 0.4.0",
        "prometheus-client >= 0.1.1",
    ],
)
