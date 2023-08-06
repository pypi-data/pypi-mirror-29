[![Build Status](https://travis-ci.org/dutradda/openapi21-python.svg?branch=master)](https://travis-ci.org/dutradda/openapi21-python)
[![Coverage Status](https://coveralls.io/repos/github/dutradda/openapi21-python/badge.svg?branch=master)](https://coveralls.io/github/dutradda/openapi21-python?branch=master)

# openapi21-python
An OpenAPI 2.1 Unofficial Specification Python Validator.

Usage example:
```shell
$ pip install openapi21
$ openapi21-validator https://cdn.rawgit.com/dutradda/OpenAPI-Specification-2.1/master/example/swagger.json
https://cdn.rawgit.com/dutradda/OpenAPI-Specification-2.1/master/example/swagger.json - OK

$ openapi21-validator my_awesome_spec.json my_other_awesome_spec.yml
my_awesome_spec.json - OK
my_other_awesome_spec.yml - OK

$ openapi21-validator my_awesome_spec.json my_other_awesome_spec.yml -t
$
```

Or inside the python code:
```python
from openapi21 import validate_spec, validate_spec_url

spec = {
    "swagger":"2.1",
    "info":{
        "version": "0.0.1",
        "title": "Store Example"
    },
    "paths": {
        "allOf": [{
            "$ref": "dresses/swagger.json"
        },{
            "$ref": "shoes/swagger.json"
        }]
    },
    "definitions": {
        "allOf": [{
            "$ref": "definitions.json"
        },{
            "$ref": "dresses/definitions.json"
        },{
            "$ref": "shoes/definitions.json"
        }]
    }
}

validate_spec(spec, spec_url='OpenAPI-Specification-2.1'
                             '/example/swagger.json')

validate_spec_url('http://cdn.rawgit.com/dutradda/'
                  'OpenAPI-Specification-2.1/master'
                  '/example/swagger.json')
```