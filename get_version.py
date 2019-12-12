#
# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Cole Clifford <c.clifford@dessa.com>, 11 2019
#

from setuptools_scm import get_version

print(get_version(
    local_scheme='dirty-tag'
))