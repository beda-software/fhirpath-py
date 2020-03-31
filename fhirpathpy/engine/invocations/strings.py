import re
import json
import fhirpathpy.engine.util as util


def ensureStringSingleton(x):
    d = util.valData(x[0])
    if len(x) == 1 and type(d) == str:
        return d

    raise Exception("Expected string, but got " + json.dumps(d))


def indexOf(coll, substr):
    string = ensureStringSingleton(coll)
    return string.index(substr)


def substring(coll, start, length):
    start = int(start)
    length = int(length)
    string = ensureStringSingleton(coll)
    return string[start : start + length]


def startsWith(coll, prefix):
    string = ensureStringSingleton(coll)
    return string.startswith(prefix)


def endsWith(coll, postfix):
    string = ensureStringSingleton(coll)
    return string.endswith(postfix)


def containsFn(coll, substr):
    string = ensureStringSingleton(coll)
    return substr in string


# test function
def matches(coll, regex):
    string = ensureStringSingleton(coll)
    valid = re.compile(regex)
    return re.search(valid, string) is not None


def replace(coll, regex, repl):
    string = ensureStringSingleton(coll)
    return string.replace(regex, repl)


def replaceMatches(coll, regex, repl):
    string = ensureStringSingleton(coll)
    valid = re.compile(regex)
    return re.sub(valid, repl, string)


def length(coll):
    str = ensureStringSingleton(coll)
    return len(str)
