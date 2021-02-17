#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of cryptidy module

"""
The cryptidy module wraps PyCrpytodome(x) functions into simple
symmetric and asymmetric functions


Versioning semantics:
    Major version: backward compatibility breaking changes
    Minor version: New functionality
    Patch version: Backwards compatible bug fixes

"""

__intname__ = 'tests.configparser_crypt'
__author__ = 'Orsiris de Jong'
__copyright__ = 'Copyright (C) 2018-2021 Orsiris de Jong'
__licence__ = 'BSD 3 Clause'
__build__ = '2021021701'

import os
from random import random

from configparser_crypt import ConfigParserCrypt


def test_ConfigParserCrypt():
    for i in range(0, 20):
        filename = 'test_{}.file'.format(int(random() * 100000))
        if os.path.exists(filename):
            os.remove(filename)

        conf_file = ConfigParserCrypt()
        conf_file.generate_key()

        if i != 0:
            conf_file.header_length = int(random() * 2048) * i
            conf_file.footer_length = int(random() * 1000) * i

        conf_file.add_section('TEST')
        conf_file['TEST']['spam'] = 'eggs'
        with open(filename, 'wb') as fp:
            conf_file.write_encrypted(fp)
        conf_file['TEST']['spam'] = 'No'
        conf_file.read_encrypted(filename)
        assert conf_file['TEST']['spam'] == 'eggs', 'Write / read of config should present same result'

        print('Test conf file size: ', os.stat(filename).st_size)
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == '__main__':
    print('Example code for %s, %s' % (__intname__, __build__))
    test_ConfigParserCrypt()
