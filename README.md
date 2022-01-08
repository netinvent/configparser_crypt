# configparser_crypt
## Drop-In replacement for ConfigParser with encrypted ini file support

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/netinvent/ofunctions.svg)](http://isitmaintained.com/project/netinvent/configparser_crypt "Percentage of issues still open")
[![Maintainability](https://api.codeclimate.com/v1/badges/683f2fd6af8fc1c8de73/maintainability)](https://codeclimate.com/github/netinvent/configparser_crypt/maintainability)
[![codecov](https://codecov.io/gh/netinvent/configparser_crypt/branch/master/graph/badge.svg?token=J7GMZYPYGQ)](https://codecov.io/gh/netinvent/configparser_crypt)
[![linux-tests](https://github.com/netinvent/configparser_crypt/actions/workflows/linux.yaml/badge.svg)](https://github.com/netinvent/configparser_crypt/actions/workflows/linux.yaml)
[![windows-tests](https://github.com/netinvent/configparser_crypt/actions/workflows/windows.yaml/badge.svg)](https://github.com/netinvent/configparser_crypt/actions/workflows/windows.yaml)
[![GitHub Release](https://img.shields.io/github/release/netinvent/configparser_crypt.svg?label=Latest)](https://github.com/netinvent/configparser_crypt/releases/latest)

configparser_crypt is a drop-in replacement for configparser, that allows to read / write encrypted configuration files.

It is compatible with Python 3.5+ and is tested on both Linux and Windows.

## Setup

```
pip install configparser_crypt

```

## Usage

Just like configparser, except that we read/write binary files and have a AES key.


How to write en encrypted config file
```
from confiparser_crypt import ConfigParserCrypt

file = 'config.encrypted'
conf_file = ConfigParsercrypt()

# Create new AES key
conf_file.generate_key()
# Don't forget to backup your key somewhere
aes_key = conf_file.aes_key

# Use like normal configparser class
conf_file.add_section('TEST')
conf_file['TEST']['foo'] = 'bar'

# Write encrypted config file
with open(file, 'wb') as file_handle:
    conf_file.write_encrypted(file_handle)
```

How to read an encrypted confi fike
```
from confiparser_crypt import ConfigParserCrypt

file = 'config.encrypted'
conf_file = ConfigParsercrypt()

# Set AES key
conf_file.aes_key = my_previously_backed_up_aes_key

# Read encrypted config file
conf_file.read_encrypted(file)
print(conf_file['TEST']['foo'])
```

The following is an example of drop-in-replacement for ConfigParser

```diff
-from configparser import ConfigParser
+from configparser_crypt import ConfigParserCrypt

file = 'config.ini'
-conf_file = ConfigParser()
+conf_file = ConfigParserCrypt()
+key = conf_file.generate_key()

# Add some values to the file
conf_file.add_section('TEST')
conf_file['TEST']['spam'] = 'eggs'

# Write config file
-with open(file, 'w') as file_handle:
-    conf_file.write(file_handle)
+with open(file, 'wb') as file_handle:
+    conf_file.write_encrypted(file_handle)

# Read from config file
-conf_file = ConfigParser()
-conf_file.read(file)
+conf_file = ConfigParserCrypt()
+conf_file.aes_key = secure_key
+conf_file.read_encrypted(file)

# Check that config file contains 'spam = eggs'
assert conf_file['TEST']['spam'] == 'eggs'
```
