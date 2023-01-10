fhirpath.py
===========

[![Build Status](https://github.com/beda-software/fhirpath-py/actions/workflows/build.yaml/badge.svg)](https://github.com/beda-software/fhirpath-py/actions)
[![codecov](https://codecov.io/gh/beda-software/fhirpath-py/branch/master/graph/badge.svg)](https://codecov.io/gh/beda-software/fhirpath-py)
[![pypi](https://img.shields.io/pypi/v/fhirpathpy.svg)](https://pypi.org/project/fhirpathpy/)
[![Supported Python version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

[FHIRPath](https://www.hl7.org/fhir/fhirpath.html) implementation in Python

Parser was generated with [antlr4](https://github.com/antlr/antlr4)

# Getting started
## Install
`pip install fhirpathpy`

## Usage
```Python
from fhirpathpy import evaluate

patient = {
  "resourceType": "Patient",
  "id": "example",
  "name": [
    {
      "use": "official",
      "given": [
        "Peter",
        "James"
      ],
      "family": "Chalmers"
    },
    {
      "use": "usual",
      "given": [
        "Jim"
      ]
    },
    {
      "use": "maiden",
      "given": [
        "Peter",
        "James"
      ],
      "family": "Windsor",
      "period": {
        "end": "2002"
      }
    }
  ]
}

# Evaluating FHIRPath
result = evaluate(patient, "Patient.name.where(use='usual').given.first()", [])
# result: `['Jim']`
```

## evaluate
 > Evaluates the "path" FHIRPath expression on the given resource, using data
    from "context" for variables mentioned in the "path" expression.
    Parameters:
    resource (dict|list): FHIR resource, bundle as js object or array of resources This resource will be modified by this function to add type information.
    path (string): fhirpath expression, sample 'Patient.name.given'
    context (dict): a hash of variable name/value pairs.
    model (dict): The "model" data object specific to a domain, e.g. R4.
    Returns:
    int: Description of return value

## compile
> Returns a function that takes a resource and an optional context hash (see
    "evaluate"), and returns the result of evaluating the given FHIRPath
    expression on that resource.  The advantage of this function over "evaluate"
    is that if you have multiple resources, the given FHIRPath expression will
    only be parsed once.
    Parameters:
    path (string) - the FHIRPath expression to be parsed.
    model (dict) - The "model" data object specific to a domain, e.g. R4.
