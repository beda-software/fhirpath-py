fhirpath.py
===========

[![Build Status](https://travis-ci.org/beda-software/fhirpath-py.svg?branch=master)](https://travis-ci.org/beda-software/fhirpath-py)
[![Supported Python version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)

[FHIRPath](https://www.hl7.org/fhir/fhirpath.html) implementation in Python

Parser was generated with [antlr4](https://github.com/antlr/antlr4) 

# Getting started
## Install
`pip install git+https://github.com/beda-software/fhirpath-py.git`

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
