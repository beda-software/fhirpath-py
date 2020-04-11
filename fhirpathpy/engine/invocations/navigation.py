from functools import reduce
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes

create_node = nodes.ResourceNode.create_node


def create_reduce_children(ctx={}):
    model = {}  # @TODO use ctx

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
                if model is not None and "pathsDefinedElsewhere" in model:
                    if value in model["pathsDefinedElsewhere"]:
                        childPath = model["pathsDefinedElsewhere"][childPath]

                if isinstance(value, list):
                    mapped = [create_node(n, childPath) for n in value]
                    acc = acc + mapped
                else:
                    acc.append(create_node(value, childPath))
        return acc

    return func


def children(coll):
    return reduce(create_reduce_children(), coll, [])


def descendants(coll):
    res = []
    ch = children(coll)
    while len(ch) > 0:
        res = res + ch
        ch = children(ch)

    return res
