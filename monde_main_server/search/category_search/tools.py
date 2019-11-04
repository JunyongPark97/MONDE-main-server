import math


def is_include(value, data):
    if value in data:
        return True
    return False


def get_data_result(category, instance):
    """
    user가 선택한 카테고리에 해당하는 instance의 카테고리 data return
    :param category: user input data에서 key값
    :param instance: ProductCategories instance
    :return:
    """
    s_data = instance.shape_result
    ch_data = instance.charm_result
    co_data = instance.colors
    d_data = instance.deco_result
    p_data = instance.pattern_result
    if category == 'shape':
        return s_data, 9.9
    elif category == 'charm':
        return ch_data, 6.2
    elif category == 'color':
        return co_data, 8.5
    elif category == 'deco':
        return d_data, 5.7
    elif category == 'pattern':
        return p_data, 6.7
    return None


def filter_type(user_input, queryset):
    types = user_input.pop('type')
    qs = queryset.filter(type_result__contains=types)
    return qs


def pass_filter(value, count):
    """
    filter 역할
    :param value: 가중치 곱해진 값
    :param count:
    :return:
    """
    result = value * math.sqrt(((count/10) + 1) * count)
    return result


def product_overlap_count(user_input, instance):
    """
    user_input을 받아 count, 가중치 계산 후 instance & 결과값 return
    """
    count = 0
    value = 0
    # weight => shape = color > pattern > charm > deco

    for category in user_input.keys():
        data, weight = get_data_result(category, instance)
        user_select = user_input[category]
        if user_select in data:
            count += 1
            value += data[user_select] * weight

    if count == 0:
        pass

    result = pass_filter(value, count)

    return instance, result


def filtered_data(instance, user_input, result_dict):
    """
    결과값을 dict형태로 바꾸는 함수
    """
    i, result = product_overlap_count(user_input, instance)
    if result != 0:
        result_dict[i] = result
    else:
        pass
    return result_dict


def search(user_input, queryset):
    qs = filter_type(user_input, queryset)
    result_dict = {}
    for q in qs:
        result_dict = filtered_data(q, user_input, result_dict)
    sorted_category_result_list = sorted(result_dict, key=lambda kv: result_dict[kv], reverse=True)
    sorted_product = list(map(lambda x: x.product, sorted_category_result_list))
    return sorted_product
