#
# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Cole Clifford <c.clifford@dessa.com>, 11 2019
#
from setuptools import setup, find_packages

with open('requirements.txt', 'r') as fp:
    install_requires = fp.read().splitlines()

setup(name='foundations-auth-proxy',
      use_scm_version = {'local_scheme': 'dirty-tag'},
      description='Foundations Authentication Proxy',
      packages=find_packages(exclude=('tests', 'docs')),
      install_requires=install_requires,
      zip_safe=False)