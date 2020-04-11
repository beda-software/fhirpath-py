import json

""" 
This file holds code to hande the FHIRPath Math functions.
"""


def contains_impl(ctx, a, b):
    # b is assumed to have one element and it tests whether b[0] is in a
    if len(b) == 0:
        return True

    for i in range(0, len(a)):
        if a[i] == b[0]:
            return True

    return False


def contains(ctx, a, b):
    if len(b) == 0:
        return []
    if len(a) == 0:
        return False
    if len(b) > 1:
        raise Exception(
            "Expected singleton on right side of contains, got " + json.dumps(b)
        )

    return contains_impl(a, b)


def inn(ctx, a, b):
    if len(a) == 0:
        return []
    if len(b) == 0:
        return False
    if len(a) > 1:
        raise Exception("Expected singleton on right side of in, got " + json.dumps(b))

    return contains_impl(b, a)
