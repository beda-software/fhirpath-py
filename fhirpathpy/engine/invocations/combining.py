import fhirpathpy.engine.invocations.existence as existence

"""
This file holds code to hande the FHIRPath Combining functions
"""


def unionOp(coll1, coll2):
    return existence.distinctFn(coll1 + coll2)


def combineFn(coll1, coll2):
    return coll1 + coll2
