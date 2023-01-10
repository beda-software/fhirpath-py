from fhirpathpy.engine.invocations.constants import constants
from fhirpathpy.parser import parse
from fhirpathpy.engine import do_eval
from fhirpathpy.engine.util import arraify, get_data, set_paths
from fhirpathpy.engine.nodes import FP_Type

__title__ = "fhirpathpy"
__version__ = "0.1.2"
__author__ = "beda.software"
__license__ = "MIT"
__copyright__ = "Copyright 2023 beda.software"

# Version synonym
VERSION = __version__


def apply_parsed_path(resource, parsedPath, context={}, model=None):
    constants.reset()
    dataRoot = arraify(resource)

    """
    do_eval takes a "ctx" object, and we store things in that as we parse, so we
    need to put user-provided variable data in a sub-object, ctx['vars'].
    Set up default standard variables, and allow override from the variables.
    However, we'll keep our own copy of dataRoot for internal processing.
    """
    vars = {"context": resource, "ucum": "http://unitsofmeasure.org"}
    vars.update(context)

    ctx = {"dataRoot": dataRoot, "vars": vars, "model": model}
    node = do_eval(ctx, dataRoot, parsedPath["children"][0])

    # Resolve any internal "ResourceNode" instances.  Continue to let FP_Type
    # subclasses through.

    def visit(node):
        data = get_data(node)

        if isinstance(node, list):
            return [visit(item) for item in data]

        if isinstance(data, dict) and not isinstance(data, FP_Type):
            for key, value in data.items():
                data[key] = visit(value)

        return data

    return visit(node)


def evaluate(resource, path, context={}, model=None):
    """
    Evaluates the "path" FHIRPath expression on the given resource, using data
    from "context" for variables mentioned in the "path" expression.

    Parameters:
    resource (dict|list): FHIR resource, bundle as js object or array of resources This resource will be modified by this function to add type information.
    path (string): fhirpath expression, sample 'Patient.name.given'
    context (dict): a hash of variable name/value pairs.
    model (dict): The "model" data object specific to a domain, e.g. R4.

    Returns:
    int: Description of return value

    """
    node = parse(path)
    return apply_parsed_path(resource, node, context, model)


def compile(path, model=None):
    """
    Returns a function that takes a resource and an optional context hash (see
    "evaluate"), and returns the result of evaluating the given FHIRPath
    expression on that resource.  The advantage of this function over "evaluate"
    is that if you have multiple resources, the given FHIRPath expression will
    only be parsed once.

    Parameters:
    path (string) - the FHIRPath expression to be parsed.
    model (dict) - The "model" data object specific to a domain, e.g. R4.

    For example, you could pass in the result of require("fhirpath/fhir-context/r4")
    """
    return set_paths(apply_parsed_path, parsedPath=parse(path), model=model)
