from fhirpathpy.engine.invocations.existence import count_fn
from fhirpathpy.engine.invocations.math import div


def avg_fn(ctx, x):
    if count_fn(ctx, x) == 0:
        return []

    return div(ctx, sum_fn(ctx, x), count_fn(ctx, x))


def sum_fn(ctx, x):
    return sum(x)


def min_fn(ctx, x):
    if count_fn(ctx, x) == 0:
        return []

    return min(x)


def max_fn(ctx, x):
    if count_fn(ctx, x) == 0:
        return []

    return max(x)


def aggregate_macro(ctx, data, expr, initial_value=None):
    ctx["$total"] = initial_value
    for i, x in enumerate(data):
        ctx["$index"] = i
        ctx["$total"] = expr(x)
    return ctx["$total"]
