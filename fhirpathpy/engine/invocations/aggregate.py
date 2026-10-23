from fhirpathpy.engine import util
from fhirpathpy.engine.invocations.existence import count_fn
from fhirpathpy.engine.invocations.math import div


def unwrap_values(x):
    """
    Returns the plain values of the input collection.

    Items coming from a resource are ResourceNode instances, so they have to be
    unwrapped (and converted, e.g. a FHIR Quantity to System.Quantity) before
    they can be used in arithmetic or comparison.
    """
    return [util.get_data(util.val_data_converted(item)) for item in x]


def avg_fn(ctx, x):
    if count_fn(ctx, x) == 0:
        return []

    return div(ctx, sum_fn(ctx, x), count_fn(ctx, x))


def sum_fn(ctx, x):
    return sum(unwrap_values(x))


def min_fn(ctx, x):
    if count_fn(ctx, x) == 0:
        return []

    return min(unwrap_values(x))


def max_fn(ctx, x):
    if count_fn(ctx, x) == 0:
        return []

    return max(unwrap_values(x))


def aggregate_macro(ctx, data, expr, initial_value=None):
    ctx["$total"] = initial_value
    for i, x in enumerate(data):
        ctx["$index"] = i
        ctx["$total"] = expr(x)
    return ctx["$total"]
