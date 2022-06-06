#! /usr/bin/env python
#  -*- coding: utf-8 -*-

# This file is part of configparser_crypt package

"""
The configparser_crypt package is a dropin replacement for configparser
that allows read/write of symmetric encrypted ini files
"""

__intname__ = "configparser_crypt.dict_convert"
__author__ = "Orsiris de Jong"
__copyright__ = "Copyright (C) 2016-2022 Orsiris de Jong"
__description__ = "Drop-in replacement for ConfigParser with encryption support"
__licence__ = "BSD 3 Clause"
__version__ = "1.0.0"
__build__ = "2022060601"

import configparser_crypt


def configparser_to_dict(config: configparser_crypt.ConfigParserCrypt) -> dict:
    config_dict = {}
    for section in config.sections():
        config_dict[section] = {}
        for key, value in config.items(section):
            # Now try to convert back to original types if possible
            for boolean in ["True", "False", "None"]:
                if value == boolean:
                    value = bool(boolean)

            # Try to convert to float or int
            try:
                if isinstance(value, str):
                    if "." in value:
                        value = float(value)
                    else:
                        value = int(value)
            except ValueError:
                pass

            config_dict[section][key] = value

    # Now drop root section if present
    config_dict.pop("root", None)
    return config_dict


def dict_to_configparser(config_dict: dict) -> configparser_crypt.ConfigParser:
    config = configparser_crypt.ConfigParserCrypt()

    for section in config_dict.keys():
        config.add_section(section)
        # Now let's convert all objects to strings so configparser is happy
        for key, value in config_dict[section].items():
            config[section][key] = str(value)

    return config
