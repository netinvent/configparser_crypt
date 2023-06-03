#! /usr/bin/env python
#  -*- coding: utf-8 -*-

# This file is part of configparser_crypt package

"""
The configparser_crypt package is a drop-in replacement for configparser
that allows read/write of symmetric encrypted ini files
"""

__intname__ = "configparser_crypt"
__author__ = "Orsiris de Jong"
__copyright__ = "Copyright (C) 2016-2022 Orsiris de Jong"
__description__ = "Drop-in replacement for ConfigParser with encryption support"
__licence__ = "BSD 3 Clause"
__version__ = "1.1.0"
__build__ = "2022102801"
__compat__ = "python3.5+"

import os
from configparser import ConfigParser

import cryptidy.symmetric_encryption as symmetric_encryption
from Cryptodome.Random import get_random_bytes


class ConfigParserCrypt(ConfigParser):
    """Configuration file parser

    A child class of configparser that reads and writes AES encrypted configuration files
    See configparser for usage

    ConfigParserCrypt behaves excactly like ConfigParser, except it has the following functions:

    aes_key = generate_key()
    set_key(aes_key)
    read_encrypted()
    write_encrypted()
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # By default, configparser sets all strings to lowercase, this option let's keep the case
        self.optionxform = str
        self.to_write_data = ""

        # AES cypto key with optional added random bytes
        self._aes_key = None
        self._header_length = 0
        self._footer_length = 0

    @property
    def aes_key(self):
        return self._aes_key

    @aes_key.setter
    def aes_key(self, aes_key):
        if len(aes_key) not in [16, 32]:
            raise ValueError(
                "AES Key should be 16 or 32 bytes, %s bytes given." % len(aes_key)
            )
        self._aes_key = aes_key

    def generate_key(self, size=32):
        """
        Generate a fresh AES 256 bits key by default (32 bytes)
        """
        try:
            self.aes_key = symmetric_encryption.generate_key(size=size)
            return self.aes_key
        except Exception as exc:
            raise ValueError("Cannot generate AES key: %s" % exc)

    @property
    def header_length(self):
        return self._header_length

    @header_length.setter
    def header_length(self, value):
        if isinstance(value, int):
            self._header_length = value
        else:
            raise ValueError("Header length must be an int")

    @property
    def footer_length(self):
        return self._footer_length

    @footer_length.setter
    def footer_length(self, value):
        if isinstance(value, int):
            self._footer_length = value
        else:
            raise ValueError("Header length must be an int")

    def read_encrypted(self, filenames, encoding=None, aes_key=None):
        """Read and parse a filename or an iterable of filenames.

        Files that cannot be opened are silently ignored; this is
        designed so that you can specify an iterable of potential
        configuration file locations (e.g. current directory, user's
        home directory, systemwide directory), and all existing
        configuration files in the iterable will be read.  A single
        filename may also be given.

        Return list of successfully read files.

        We'll keep unused encoding= attribute to be 100% compatible with non encrypted read() function
        """

        # ConfigParser for python < 3.6 does not use os.PathLike since it does not exist
        # Fallback to earlier implementation
        try:
            if isinstance(filenames, (str, bytes, os.PathLike)):
                filenames = [filenames]
        except AttributeError:
            if isinstance(filenames, str):
                filenames = [filenames]

        read_ok = []
        for filename in filenames:
            try:
                with open(filename, "rb") as file_handle:
                    self._read_encrypted(file_handle, filename, aes_key)
            except OSError:
                continue
            # Same here, we'll get a AttributeError since os.fspath does not exist in Python 3.5
            # Original ConfigParser did not have that part of the code, let's fallback to ignoring it
            try:
                if isinstance(filename, os.PathLike):
                    filename = os.fspath(filename)
            except AttributeError:
                pass
            read_ok.append(filename)
        return read_ok

    def _read_encrypted(self, file_handle, filename, aes_key):
        try:
            if aes_key is None and self.aes_key is None:
                raise ValueError("No aes key provided.")
            if aes_key is None:
                # on the fly provided aes key has precedence over class aes key
                aes_key = self.aes_key
            _, raw_data = symmetric_encryption.decrypt_message_hf(
                file_handle.read(),
                aes_key,
                random_header_len=self._header_length,
                random_footer_len=self._footer_length,
            )
            # Don't keep optional aes_key in memory if not needed
            aes_key = None
            data = raw_data.decode("utf-8").split("\n")
        except Exception as exc:
            raise ValueError("Cannot read AES data: %s" % exc)
        self._read(data, filename)

    def write_encrypted(self, file_handle, space_around_delimiters=True, aes_key=None):
        """Write an .ini-format representation of the configuration state.

        If `space_around_delimiters' is True (the default), delimiters
        between keys and values are surrounded by spaces.
        """

        self.to_write_data = ""

        if space_around_delimiters:
            delim = " {} ".format(self._delimiters[0])
        else:
            delim = self._delimiters[0]
        if self._defaults:
            self._write_section_encrypted(
                self.default_section, self._defaults.items(), delim
            )
        for section in self._sections:
            self._write_section_encrypted(
                section, self._sections[section].items(), delim
            )

        self.commit_write(file_handle, aes_key=aes_key)

    def _write_section_encrypted(self, section_name, section_items, delimiter):
        """Write a single section to the specified `fp'."""
        self.to_write_data += "[{}]\n".format(section_name)
        for key, value in section_items:
            value = self._interpolation.before_write(self, section_name, key, value)
            if value is not None or not self._allow_no_value:
                value = delimiter + str(value).replace("\n", "\n\t")
            else:
                value = ""
            self.to_write_data += "{}{}\n".format(key, value)
        self.to_write_data += "\n"

    def commit_write(self, file_handle, aes_key=None):
        try:
            data = self.to_write_data.encode("utf-8")
            if aes_key is None and self.aes_key is None:
                raise ValueError("No aes key provided.")
            if aes_key is None:
                # on the fly provided aes key has precedence over class aes key
                aes_key = self.aes_key
            enc = symmetric_encryption.encrypt_message_hf(
                data,
                aes_key,
                random_header_len=self._header_length,
                random_footer_len=self._footer_length,
            )
            aes_key = None
            file_handle.write(enc)
        except Exception as exc:
            raise ValueError("Cannot write AES data: %s" % exc)
