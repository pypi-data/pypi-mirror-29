#! /usr/share/env python
# -*- coding:utf-8 -*-

# This file is a part of IoT-LAB radio test code
# Copyright (C) 2017 INRIA (Contact: admin@iot-lab.info)
# Contributor(s) : see AUTHORS file
#
# This software is governed by the CeCILL license under French law
# and abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# http://www.cecill.info.
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""setup.py deployement script.

"""

from setuptools import setup, find_packages

import os

PACKAGE = 'iotlab_radio_test'
# GPL compatible http://www.gnu.org/licenses/license-list.html#CeCILL
LICENSE = 'CeCILL v2.1'


def get_version(package):
    """Extract package version without importing file.

    Importing cause issues with coverage,
        (modules can be removed from sys.modules to prevent this)
    Importing __init__.py triggers importing rest and then requests too

    Inspired from pep8 setup.py
    """
    with open(os.path.join(package, '__init__.py')) as init_fd:
        for line in init_fd:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])  # pylint:disable=eval-used


INSTALL_REQUIRES = ['namedlist', 'numpy', 'matplotlib', 'iotlabcli', 'pyyaml', 'flask', 'psutil']

setup(name=PACKAGE,
      version=get_version(PACKAGE),
      description='Nodes Radio Test',
      author='IoT-Lab Team',
      author_email='admin@iot-lab.info',
      url='http://www.iot-lab.info',
      license=LICENSE,
      packages=find_packages(),
      package_data={'firmwares': ['firmwares/*']},
      include_package_data=True,
      entry_points={
          'console_scripts': ['iotlab-radiotest=iotlab_radio_test.cli:main'],
      },

      install_requires=INSTALL_REQUIRES)
