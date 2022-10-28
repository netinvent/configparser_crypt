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

It is compatible with Python 3.5+/PyPy and is tested on both Linux and Windows.

## Setup

```
pip install configparser_crypt

```

## Usage

Just like configparser, except that we read/write binary files and have a AES key.
AES key generation is done using `generate_key()` which by default generates a 256-bit encryption key.
You may also generate a 128 or 192 bit key by giving the byte length as parameter (16, 24 or 32 bytes).


How to write en encrypted config file
```python
from configparser_crypt import ConfigParserCrypt

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

How to read an encrypted config file
```python
from configparser_crypt import ConfigParserCrypt

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

## Load an encryption key to open an encrypted config file

In order to open earlier written encrypted configuration files, you need to store the aes key generated with `aes_key = conf_file.generate_key()`.
You can than later use it by loading it into the class:
```python
file = 'my_encrypted.conf'
conf_file = ConfigParserCrypt()
conf_file.aes_key = 'PUT YOUR PREVIOUSLY GENERATED AES KEY HERE'
+conf_file.read_encrypted(file)
```

## Convert a plain ini file to encrypted version and vice-versa

It's pretty simple to encrypt an existing .ini file.
You just need to read it as standard ini file, then write it as encrypted file.

```python
original_file = 'config.ini'
target_encrypted_file = 'config.encrypted'

conf_file = ConfigParsercrypt()

# Create new AES key
conf_file.generate_key()
# Don't forget to backup your key somewhere for later usage
aes_key = conf_file.aes_key

# Read original file
config_file.read(original_file)
# Write encrypted config file
with open(target_encrypted_file, 'wb') as file_handle:
    conf_file.write_encrypted(file_handle)
```

Just keep in mind that secure deletion of the original file is out of scope of ConfigParserCrypt.
Of course, you can also read an encrypted file and save it as non encrypted.

## Convert ConfigParser to dictionary and vice-versa

Just like ConfigParser, ConfigParserCrypt provides a ConfigParser object.
It's sometimes useful to switch between those objects and a dictionary.

ConfigParserCrypt has configparser to dict and dict to configparser object functions included.
Since ConfigParser stores all variables (int, float, bool) as strings, the converter functions try to recast the original type of the variable when rendering a dictionary.

The only drawback is that your dictionaries must not exceed more than two level depth, eg:
```python
my_dict = {
    'section_name':
        {
            'some_name': 'some_var'
        },
    'another_section':
        {
            'another_var': 'something',
            'an int': 1,
            'a bool': False
        }
}
```

Note that these convert functions also work with vanilla ConfigPaser
Example:
```python

import ConfigParserCrypt
from configparser_crypt.dict_convert import configparser_to_dict, dict_to_configparser

my_dict = configparser_to_dict(configparser_object)
type(my_dict['some_int']) == True

my_config_parser_object = dict_to_configparser(some_dict)
```
