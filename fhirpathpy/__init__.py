from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, TypeAlias, TypeVar, cast

from fhirpathpy.engine import do_eval
from fhirpathpy.engine.invocations.constants import constants
from fhirpathpy.engine.nodes import FP_Type, ResourceNode
from fhirpathpy.engine.util import arraify, get_data, process_user_invocation_table, set_paths
from fhirpathpy.parser import parse

__title__ = "fhirpathpy"
__version__ = "2.1.0"
__author__ = "beda.software"
__license__ = "MIT"
__copyright__ = "Copyright 2025 beda.software"

# Version synonym
VERSION = __version__

ResourceType: TypeAlias = Mapping[str, Any]
ContextType: TypeAlias = Mapping[str, Any] | None


def apply_parsed_path(resource, parsedPath, context=None, model=None, options=None):
    constants.reset()
    dataRoot = arraify(resource)

    """
    do_eval takes a "ctx" object, and we store things in that as we parse, so we
    need to put user-provided variable data in a sub-object, ctx['vars'].
    Set up default standard variables, and allow override from the variables.
    However, we'll keep our own copy of dataRoot for internal processing.
    """
    vars = {"context": resource, "ucum": "http://unitsofmeasure.org"}
    vars.update(context or {})

    ctx = {
        "dataRoot": dataRoot,
        "vars": vars,
        "model": model,
        "userInvocationTable": process_user_invocation_table(
            (options or {}).get("userInvocationTable", {})
        ),
    }

    # Add trace callback if provided in options
    if options and "traceFn" in options:
        ctx["traceFn"] = options["traceFn"]

    node = do_eval(ctx, dataRoot, parsedPath["children"][0])

    # Resolve any internal "ResourceNode" instances.  Continue to let FP_Type
    # subclasses through.

    if options and options.get("returnRawData", False):
        if isinstance(node, list):
            res = []
            # Filter out intenal representation of primitive extensions
            # even in this raw data mode (as they are not a part of the output)
            for item in node:
                if isinstance(item, ResourceNode):
                    if isinstance(item.data, dict):
                        keys = list(item.data.keys())
                        if keys == ["extension"]:
                            continue
                res.append(item)
            return res
        return node

    def visit(node):
        data = get_data(node)

        if isinstance(node, list):
            res = []
            for item in data:
                # Filter out intenal representation of primitive extensions
                i = visit(item)
                if isinstance(i, dict):
                    keys = list(i.keys())
                    if keys == ["extension"]:
                        continue
                res.append(i)
            return res

        if isinstance(data, dict) and not isinstance(data, FP_Type):
            for key, value in data.items():
                data[key] = visit(value)

        return data

    return visit(node)


def evaluate(
    resource: ResourceType | list,
    path: str | dict,
    context: dict | None = None,
    model: dict | None = None,
    options: dict | None = None,
) -> list:
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
    if isinstance(path, dict):
        node = parse(path["expression"])
        if "base" in path:
            resource = ResourceNode.create_node(resource, path["base"])
    else:
        node = parse(path)

    return apply_parsed_path(resource, node, context or {}, model, options)


def compile(
    path: str, model: dict | None = None, options: dict | None = None
) -> Callable[[ResourceType, ContextType], list]:
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
    return set_paths(apply_parsed_path, parsedPath=parse(path), model=model, options=options)


InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


def compile_as_array(
    expression: str, input_type: type[InputType], output_type: type[OutputType]
) -> Callable[[InputType, ContextType], list[OutputType]]:
    path_fn = compile(expression)

    def fn(resource: Any, context: ContextType = None) -> Any:
        return _format_result(
            path_fn(_prepare_data(resource, input_type), context),
            output_type,
            is_array=True,
        )

    return cast(Callable[[InputType, ContextType], list[OutputType]], fn)


def compile_as_first(
    expression: str, input_type: type[InputType], output_type: type[OutputType]
) -> Callable[[InputType, ContextType], OutputType | None]:
    path_fn = compile(expression)

    def fn(resource: Any, context: ContextType = None) -> Any:
        return _format_result(
            path_fn(_prepare_data(resource, input_type), context),
            output_type,
            is_array=False,
        )

    return cast(Callable[[InputType, ContextType], OutputType | None], fn)


def _prepare_data(resource: Any, input_type: type[InputType]) -> ResourceType:
    if not isinstance(resource, input_type):
        raise Exception(
            f"Resource type is {type(resource).__name__}, expected {input_type.__name__}"
        )

    if isinstance(resource, dict):
        return resource

    if hasattr(resource, "model_dump"):
        return resource.model_dump()

    raise Exception(f"Don't know how to work with type {type(resource).__name__}")


def _format_result(result: list, output_type: type[OutputType], is_array=False) -> Any:
    result = [_format_item(item, output_type) for item in result]

    if is_array:
        return result

    if len(result) == 0:
        return None

    return result[0]


def _format_item(item: Any, output_type: type[OutputType]) -> OutputType:
    if hasattr(output_type, "model_validate"):
        return cast(Any, output_type).model_validate(item)

    if not isinstance(item, output_type):
        raise Exception(
            f"Expected result to be {output_type.__name__}, but got {type(item).__name__}"
        )

    return item
