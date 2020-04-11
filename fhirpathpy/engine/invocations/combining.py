import fhirpathpy.engine.invocations.existence as existence

"""
This file holds code to hande the FHIRPath Combining functions
"""


def union_op(coll1, coll2):
    return existence.distinct_fn(coll1 + coll2)


def combine_fn(coll1, coll2):
    return coll1 + coll2
