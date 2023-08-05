from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django_payload_validator',
    version='1.0.1',
    description='validator for django payload',
    long_description=long_description,
    url='https://github.com/gladsonvm/django_payload_validator',
    author='Gladson V Manuel',
    author_email='gladsonvm@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django payload validator intended audience is dev',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['django']
)
