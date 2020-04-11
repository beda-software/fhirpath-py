def or_op(ctx, a, b):
    if isinstance(b, list):
        if a == True:
            return True
        if a == False:
            return []
        if isinstance(a, list):
            return []
    if isinstance(a, list):
        if b == True:
            return True
        return []

    return a or b


def and_op(ctx, a, b):
    if isinstance(b, list):
        if a == True:
            return []
        if a == False:
            return False
        if isinstance(a, list):
            return []

    if isinstance(a, list):
        if b == True:
            return []
        return False

    return a and b


def xor_op(ctx, a, b):
    # If a or b are arrays, they must be the empty set.
    # In that case, the result is always the empty set.
    if isinstance(a, list) or isinstance(b, list):
        return []

    return (a and not b) or (not a and b)


def implies_op(ctx, a, b):
    if isinstance(b, list):
        if a == True:
            return []
        if a == False:
            return True
        if isinstance(a, list):
            return []

    if isinstance(a, list):
        if b == True:
            return True
        return []

    if a == False:
        return True

    return a and b
