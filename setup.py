from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='api-base',
    url='https://github.com/mpalazzolo/api-base',
    version='1.0.0',
    packages=['apibase'],
    license='LICENSE.txt',
    author='Matt Palazzolo',
    author_email='mattpalazzolo@gmail.com',
    description='A base class to be used when building a python API interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests>=2.21.0'
    ],
)
