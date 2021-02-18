# configparser_crypt
## Drop-In replacement for ConfigParser with encrypted ini file support

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/netinvent/ofunctions.svg)](http://isitmaintained.com/project/netinvent/configparser_crypt "Percentage of issues still open")

## Setup

```
pip install configparser_crypt

```

## Usage

Just like configparser, except that we read/write binary files and have a AES key.


configparser example
```diff
-from configparser import ConfigParser
+from configparser_crypt import ConfigParserCrypt

file = 'config.ini'
-conf_file = ConfigParser()
+conf_file = ConfigParserCrypt()

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
