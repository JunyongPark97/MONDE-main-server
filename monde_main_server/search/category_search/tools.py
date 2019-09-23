import json
import math

from products.models import CategoryCategories


def is_include(value, data):
    if value in data:
        return True
    return False


def get_data_result(category, instance):
    """
    user가 선택한 카테고리에 해당하는 instance의 카테고리 data return
    :param category: user input data에서 key값
    :param instance:
    :return:
    """
    s_data = instance.shape_result
    h_data = instance.handle_result
    ch_data = instance.charm_result
    co_data = instance.color_result
    d_data = instance.deco_result
    p_data = instance.pattern_result
    if category == 'shape':
        return(s_data)
    elif category == 'handle':
        return(h_data)
    elif category == 'charm':
        return(ch_data)
    elif category == 'color':
        return(co_data)
    elif category == 'deco':
        return(d_data)
    elif category == 'pattern':
        return(p_data)
    return None


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
    :param user_input:
    :param instance:
    :return:
    """
    count = 0
    value = 0
    weight = 2

    for category in user_input.keys():
        data = get_data_result(category, instance)
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
    :param instance:
    :param user_input:
    :param result_dict: 사용법 result_dict = filtered_data(i, user_input, result_dict)
    :return:
    """
    i, result = product_overlap_count(user_input, instance)
    if result != 0:
        result_dict[i] = result
    else:
        pass
    return result_dict


def get_searched_data(queryset, user_input):
    result_dict = {}

    for instance in queryset:
        result_dict = filtered_data(instance, user_input, result_dict)
    sorted_category_result_list = sorted(result_dict, key=lambda kv: result_dict[kv], reverse=True)
    sorted_product_result_id = list(map(lambda x: x.bag_image.product.id, sorted_category_result_list))
    return sorted_product_result_id





