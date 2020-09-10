import itertools
from functools import reduce
from fhirpathpy.engine.nodes import ResourceNode


def get_data(value):
    if isinstance(value, ResourceNode):
        return value.data
    return value


def is_number(value):
    return isinstance(value, (int, float, complex)) and not isinstance(value, bool)


def is_capitalized(x):
    return isinstance(x, str) and x[0] == x[0].upper()


def is_empty(x):
    return isinstance(x, list) and len(x) == 0


def is_some(x):
    return x is not None and not is_empty(x)


def is_nullable(x):
    return x is None or is_empty(x)


def is_true(x):
    return x is True or isinstance(x, list) and len(x) == 1 and x[0] is True


def arraify(x, instead_none=None):
    if isinstance(x, list):
        return x
    if is_some(x):
        return [x]
    return [] if instead_none is None else [instead_none]


def flatten(x):
    def func(acc, x):
        if isinstance(x, list):
            acc = acc + x
        else:
            acc.append(x)

        return acc

    return reduce(func, x, [])


def peek_iterator(iterable):
    """
    :param iterable: iterable object
    :return: If after call next of iterator raise StopIteration function returns none what means iterator is empty,
    else function returns new iterator with first element back
    """
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return itertools.chain([first], iterable)
