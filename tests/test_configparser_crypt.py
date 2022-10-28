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

__intname__ = "tests.configparser_crypt"
__author__ = "Orsiris de Jong"
__copyright__ = "Copyright (C) 2018-2022 Orsiris de Jong"
__licence__ = "BSD 3 Clause"
__build__ = "2022102801"

import os
from random import random

from configparser_crypt import ConfigParserCrypt


def test_readme_example_configparser():
    from configparser import ConfigParser

    file = "config.ini"
    if os.path.exists(file):
        os.remove(file)
    conf_file = ConfigParserCrypt()

    # Add some values to the file
    conf_file.add_section("TEST")
    conf_file["TEST"]["spam"] = "eggs"

    # Write config file
    with open(file, "w") as file_handle:
        conf_file.write(file_handle)

    # Read from config file
    conf_file = ConfigParser()
    conf_file.read(file)

    # Check that config file contains 'spam = eggs'
    assert conf_file["TEST"]["spam"] == "eggs"

    if os.path.exists(file):
        os.remove(file)


def test_readme_example_configparser_crypt():
    from configparser_crypt import ConfigParserCrypt

    file = "config.ini"
    if os.path.exists(file):
        os.remove(file)
    conf_file = ConfigParserCrypt()
    secure_key = conf_file.generate_key()

    # Add some values to the file
    conf_file.add_section("TEST")
    conf_file["TEST"]["spam"] = "eggs"

    # Write config file
    with open(file, "wb") as file_handle:
        conf_file.write_encrypted(file_handle)

    # Read from config file
    conf_file = ConfigParserCrypt()
    conf_file.aes_key = secure_key
    conf_file.read_encrypted(file)

    # Check that config file contains 'spam = eggs'
    assert conf_file["TEST"]["spam"] == "eggs"

    if os.path.exists(file):
        os.remove(file)


def test_ConfigParserCrypt():
    for i in range(0, 20):
        filename = "test_{}.file".format(int(random() * 100000))
        if os.path.exists(filename):
            os.remove(filename)

        conf_file = ConfigParserCrypt()
        conf_file.generate_key()

        # Let's keep default values (zero) for the fist test
        if i != 0:
            conf_file.header_length = int(random() * 2048) * i
            conf_file.footer_length = int(random() * 1000) * i

        conf_file.add_section("TEST")
        conf_file["TEST"]["spam"] = "eggs"
        with open(filename, "wb") as fp:
            conf_file.write_encrypted(fp)
        conf_file["TEST"]["spam"] = "No"
        conf_file.read_encrypted(filename)
        assert (
            conf_file["TEST"]["spam"] == "eggs"
        ), "Write / read of config should present same result"

        print("Test conf file size: ", os.stat(filename).st_size)
        if os.path.exists(filename):
            os.remove(filename)


def test_special_chars_test():
    """
    Make sure input and output are identical
    By default, ConfigParser needs %% to represent '%' char
    using interpolation=None disables specific handling of '%' char
    """
    special_string = r'+oy%#"Xd2EYKc9Gb@u'

    filename = "test_{}.file".format(int(random() * 100000))
    if os.path.exists(filename):
        os.remove(filename)

    conf_file = ConfigParserCrypt(interpolation=None)
    conf_file.generate_key()

    conf_file.add_section("TEST")
    conf_file["TEST"]["special_string"] = special_string


    with open(filename, "wb") as fp:
        conf_file.write_encrypted(fp)
    conf_file["TEST"]["special_string"] = "No"
    conf_file.read_encrypted(filename)
    assert (
        conf_file["TEST"]["special_string"] == special_string
    ), "Write / read of config should present same result"

    print("Test conf file size: ", os.stat(filename).st_size)
    if os.path.exists(filename):
        os.remove(filename)


if __name__ == "__main__":
    print("Example code for %s, %s" % (__intname__, __build__))
    test_readme_example_configparser()
    test_readme_example_configparser_crypt()
    test_ConfigParserCrypt()
