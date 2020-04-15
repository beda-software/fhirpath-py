from functools import reduce
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes

create_node = nodes.ResourceNode.create_node


def create_reduce_children(ctx):
    model = ctx["model"]

    def func(acc, res):
        data = util.get_data(res)
        res = create_node(res)

        if isinstance(data, list):
            data = dict((i, data[i]) for i in range(0, len(data)))

        if isinstance(data, dict):
            for prop in data.keys():
                value = data[prop]
                childPath = ""

                if res.path is not None:
                    childPath = res.path + "." + prop

                if (
                    isinstance(model, dict)
                    and "pathsDefinedElsewhere" in model
                    and childPath in model["pathsDefinedElsewhere"]
                ):
                    childPath = model["pathsDefinedElsewhere"][childPath]

                if isinstance(value, list):
                    mapped = [create_node(n, childPath) for n in value]
                    acc = acc + mapped
                else:
                    acc.append(create_node(value, childPath))
        return acc

    return func


def children(ctx, coll):
    return reduce(create_reduce_children(ctx), coll, [])


def descendants(ctx, coll):
    res = []
    ch = children(ctx, coll)
    while len(ch) > 0:
        res = res + ch
        ch = children(ctx, ch)

    return res
