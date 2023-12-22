from fhirpathpy.engine.nodes import TypeInfo

def type_fn(ctx, coll):
    return [TypeInfo.from_value(value).__dict__ for value in coll]


def is_fn(ctx, coll, type_info):
    # TODO: It's incorrect place to setup model. Fix it.
    TypeInfo.model = ctx.get("model")
    if not coll:
        return []
    if len(coll) > 1:
        raise ValueError(f"Expected singleton on left side of 'is', got {coll}")
    return TypeInfo.from_value(coll[0]).is_(type_info)


def as_fn(ctx, coll, type_info):
    TypeInfo.model = ctx.get("model")
    if not coll:
        return []
    if len(coll) > 1:
        raise ValueError(f"Expected singleton on left side of 'as', got {coll}")
    return coll if TypeInfo.from_value(coll[0]).is_(type_info) else []
