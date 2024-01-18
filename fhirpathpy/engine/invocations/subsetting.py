def intersect_fn(ctx, list_1, list_2):
    intersection = []

    for obj1 in list_1:
        for obj2 in list_2:
            if obj1 == obj2:
                intersection.append(obj1)
                break

    unique_intersection = []
    for obj in intersection:
        if obj not in unique_intersection:
            unique_intersection.append(obj)

    return unique_intersection
