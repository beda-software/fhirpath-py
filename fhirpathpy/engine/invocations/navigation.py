from collections import abc
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

        if isinstance(data, abc.Mapping):
            for prop in data.keys():
                value = data[prop]
                childPath = ""

                if res.path is not None:
                    childPath = res.path + "." + prop

                fullPath = f"{res.propName}.{prop}" if res.propName else childPath # The full path to the node (weill evenutally be) e.g. Patient.name[0].given
                fullPath = fullPath.replace("_", "")

                if prop == "extension":
                    childPath = "Extension"

                if (
                    isinstance(model, dict)
                    and "pathsDefinedElsewhere" in model
                    and childPath in model["pathsDefinedElsewhere"]
                ):
                    childPath = model["pathsDefinedElsewhere"][childPath]

                childPath = (
                    model["path2Type"].get(childPath, childPath)
                    if isinstance(model, dict) and "path2Type" in model
                    else childPath
                )
                
                if isinstance(value, list):
                    mapped = [create_node(n, childPath, propName=f"{fullPath}[{i}]") for i, n in enumerate(value)]
                    acc = acc + mapped
                else:
                    acc.append(create_node(value, childPath, propName=fullPath))
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
