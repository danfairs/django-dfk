import os
from setuptools import setup, find_packages

version = '0.0.4'

setup(
    name='django-dfk',
    description="Deferred foreign keys for Django",
    version=version,
    long_description=open("README.rst").read() + "\n" +
    	             open(os.path.join("docs", "HISTORY.rst")).read(),
    author='Dan Fairs',
    author_email='dan@fezconsulting.com',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License"
        ],
)
