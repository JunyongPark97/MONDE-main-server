import json
from products.models import CategoryCategories

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
        return True
    except ValueError as e:
        return False


def category_search_v1(data):
    # categories = list(data.keys())
    shape = data['shape']
    print(shape)
    list = []
    for category in CategoryCategories.objects.all():
        c_shape, shape_value = get_max_key(category.shape_result)
        if c_shape == shape:
            list.append(category.bag_image.product)

    return list



def get_category_keys(instance):
    max_shape, shape_value = get_max_key(instance.shape_result)
    max_handle, handle_value = get_max_key(instance.handle_result)
    max_color, color_value = get_max_key(instance.handle_color)
    max_charm, charm_value = get_max_key(instance.handle_charm)
    max_deco, deco_value = get_max_key(instance.handle_deco)
    max_pattern, pattern_value = get_max_key(instance.handle_pattern)
    return (max_shape, max_handle, max_color, max_charm, max_deco, max_pattern)


def get_max_key(data):
    # res = sorted(shape_dict.items(), key=(lambda x: x[1]), reverse=True)
    max_res = max(data.keys(), key=(lambda k: data[k]))
    value = data[max_res]
    return max_res, value
