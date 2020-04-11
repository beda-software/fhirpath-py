import re
import json
import fhirpathpy.engine.util as util


def ensure_string_singleton(x):
    d = util.get_data(x[0])
    if len(x) == 1 and type(d) == str:
        return d

    raise Exception("Expected string, but got " + json.dumps(d))


def index_of(coll, substr):
    string = ensure_string_singleton(coll)
    return string.index(substr)


def substring(coll, start, length):
    start = int(start)
    length = int(length)
    string = ensure_string_singleton(coll)
    return string[start : start + length]


def starts_with(coll, prefix):
    string = ensure_string_singleton(coll)
    return string.startswith(prefix)


def ends_with(coll, postfix):
    string = ensure_string_singleton(coll)
    return string.endswith(postfix)


def contains_fn(coll, substr):
    string = ensure_string_singleton(coll)
    return substr in string


# test function
def matches(coll, regex):
    string = ensure_string_singleton(coll)
    valid = re.compile(regex)
    return re.search(valid, string) is not None


def replace(coll, regex, repl):
    string = ensure_string_singleton(coll)
    return string.replace(regex, repl)


def replace_matches(coll, regex, repl):
    string = ensure_string_singleton(coll)
    valid = re.compile(regex)
    return re.sub(valid, repl, string)


def length(coll):
    str = ensure_string_singleton(coll)
    return len(str)
