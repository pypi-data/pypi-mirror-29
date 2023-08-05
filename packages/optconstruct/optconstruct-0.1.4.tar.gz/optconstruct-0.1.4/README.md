# Option Construct Package (opt_construct)

Package for construct options of Messaging Clients or Ansible based on prefix and input data.  

## Build/Test Status
[![Build Status](https://travis-ci.org/Frawless/optconstruct.svg?branch=master)](https://travis-ci.org/Frawless/optconstruct)
[![GitHub Issues](https://img.shields.io/github/issues/Frawless/optconstruct.svg)](https://github.com/Frawless/optconstruct/issues)
[![GitHub Issues](https://img.shields.io/github/issues-pr/Frawless/optconstruct.svg)](https://github.com/Frawless/optconstruct/pulls)
[![pypi](https://img.shields.io/pypi/v/opt_construct.svg)](https://github.com/Frawless/optconstruct)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## Description
This package provides an API for create appropriate option for command to execute in your application. API is called by one of several classes, which each of them handle different type of option.

### Example
Exmaple of Toggle class:
```
data = {'help':True}
obj = Toggle('help','--help')
opt = obj.generate(data)   
print(opt)
    ->  ['--help']
```

In current version there are these classes:
* **Toggle** - Create option only from prefix.
* **Dummy** - Only placeholder for specific values.
* **Argument** - Create option only from value.
* **Prefixed** - Create option with prefix and input value.
* **BasicComposed** - Composing multiple value into one option. You must override generate method for your own use.
* **KWOption** - Parse a dictionary into multiple appearance of one option with prefix and value.
* **ListOption** - Parse a list into multiple appearance of one option with prefix and value. 

## Requirements
Python >= 3.5

[reformat](https://bitbucket.org/zkraus/reformat)

## Install & Run
Not yet uploaded to pypi.

## Tests

### Requirements
[pytest](https://docs.pytest.org/en/latest/)

### How to run tests
```bash
$ python -m pytest tests/ 
```

## License
Apache 2.0

## Author Information
Messaging QE team @ redhat.com
