import re
import fhirpathpy.engine.util as util


def ensure_string_singleton(x):
    if len(x) == 1:
        d = util.get_data(x[0])
        if type(d) == str:
            return d
        raise Exception("Expected string, but got " + str(d))

    raise Exception("Expected string, but got " + str(x))


def index_of(ctx, coll, substr):
    string = ensure_string_singleton(coll)
    return string.find(substr)


def substring(ctx, coll, start, length=None):
    string = ensure_string_singleton(coll)
    start = int(start)

    if length is None:
        return string[start:]

    length = int(length)
    return string[start : start + length]


def starts_with(ctx, coll, prefix):
    string = ensure_string_singleton(coll)
    return string.startswith(prefix)


def ends_with(ctx, coll, postfix):
    string = ensure_string_singleton(coll)
    return string.endswith(postfix)


def contains_fn(ctx, coll, substr):
    string = ensure_string_singleton(coll)
    return substr in string


# test function
def matches(ctx, coll, regex):
    string = ensure_string_singleton(coll)
    valid = re.compile(regex)
    return re.search(valid, string) is not None


def replace(ctx, coll, regex, repl):
    string = ensure_string_singleton(coll)
    return string.replace(regex, repl)


def replace_matches(ctx, coll, regex, repl):
    string = ensure_string_singleton(coll)
    valid = re.compile(regex)
    return re.sub(valid, repl, string)


def length(ctx, coll):
    str = ensure_string_singleton(coll)
    return len(str)
