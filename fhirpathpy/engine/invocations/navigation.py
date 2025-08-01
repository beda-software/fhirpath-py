from collections import abc
from functools import reduce
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes

create_node = nodes.ResourceNode.create_node


def create_reduce_children(ctx, exclude_primitive_extensions):
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

                # extensions shouldn't filter through here, yet they should for descendants?
                # unless this item is the node that is being processed (primitive extension)
                # though if you filter it, descendants will not work too
                if prop.startswith("_") and exclude_primitive_extensions:
                    continue

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

                # If the prop tolower ends with the type tolower
                if prop.lower().endswith(childPath.lower()) and len(prop) > len(childPath):
                    # Check if the path is actually in the choice types
                    altPropName = res.path + "." + prop[:-len(childPath)]
                    actualTypes = model["choiceTypePaths"].get(altPropName, [])
                    if len(actualTypes) > 0:
                        # If it is, we can use it
                        fullPath = f"{res.propName}.{prop[:-len(childPath)]}"

                if isinstance(value, list):
                    mapped = [create_node(n, childPath, propName=f"{fullPath}[{i}]", index=i) for i, n in enumerate(value)]
                    acc = acc + mapped
                else:
                    acc.append(create_node(value, childPath, propName=fullPath))
        return acc

    return func


def children(ctx, coll):
    return reduce(create_reduce_children(ctx, True), coll, [])


def descendants(ctx, coll):
    res = []
    ch = reduce(create_reduce_children(ctx, False), coll, [])
    while len(ch) > 0:
        res = res + ch
        ch = reduce(create_reduce_children(ctx, False), ch, [])
    return res
