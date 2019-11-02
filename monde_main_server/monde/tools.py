
def get_tab_ids(tab_no, categories_queryset):

    if tab_no == 1:
        # 버킷백
        bucket_ids = get_bucket_ids(categories_queryset)
        #TODO : 정렬시 정확도순으로 해야하나? 안해도 되면 정렬이 빨라짐
        return bucket_ids

    elif tab_no == 2:
        # 크로스백
        crossbag_ids = get_crossbag_ids(categories_queryset)
        # crossbag_products = queryset.filter(pk__in=cross_ids)
        return crossbag_ids

    elif tab_no == 3:
        # 숄더백
        shoulder_ids = get_shoulder_ids(categories_queryset)
        # shoulder_products = queryset.filter(pk__in=shoulder_ids)
        return shoulder_ids

    elif tab_no == 4:
        # 클러치백 & 미니백
        clutch_ids = get_clutch_ids(categories_queryset)
        # clutch_products = queryset.filter(pk__in=clutch_ids)
        return clutch_ids

    elif tab_no == 5:
        # 토트백
        tote_ids = get_tote_ids(categories_queryset)
        # tote_products = queryset.filter(pk__in=tote_ids)
        return tote_ids

    elif tab_no == 6:
        # 백팩
        backpack_ids = get_backpack_ids(categories_queryset)
        # tote_products = queryset.filter(pk__in=tote_ids)
        return backpack_ids

    else:
        return other_ids(categories_queryset)


def get_bucket_ids(queryset):
    ids = []
    """
    ids 를 return하는 이유는 쿼리셋을 만들기 위함. list에 담아서 주지 않기 위헤
    """
    for instance in queryset:
        shape_data = instance.shape_result
        if 'bucket' in shape_data and shape_data['bucket'] > 0.5:
            ids.append(instance.product_id)

    return ids


def get_crossbag_ids(queryset):
    ids = []
    for instance in queryset:
        type_data = instance.type_result
        if 'cross_bag' in type_data and type_data['cross_bag'] > 0.4:
            ids.append(instance.product_id)
    return ids


def get_shoulder_ids(queryset):
    ids = []
    for instance in queryset:
        type_result = instance.type_result
        if 'big_shoulder' in type_result and type_result['big_shoulder'] > 0.4:
            ids.append(instance.product_id)
    return ids


def get_clutch_ids(queryset):
    ids = []
    for instance in queryset:
        type_result = instance.type_result
        if 'clutch' in type_result and type_result['clutch_bag'] > 0.5:
            ids.append(instance.product_id)
    return ids


def get_tote_ids(queryset):
    ids = []
    for instance in queryset:
        type_result = instance.type_result
        if 'hand_bag' in type_result and type_result['hand_bag'] > 0.4:
            ids.append(instance.product_id)
    return ids


def get_backpack_ids(queryset):
    ids = []
    for instance in queryset:
        type_result = instance.type_result
        if 'backpack' in type_result and type_result['backpack'] > 0.4:
            ids.append(instance.product_id)
    return ids


def other_ids(queryset):
    ids = []
    for instance in queryset:
        ids.append(instance.product_id)
    return ids


def filter_by_famous(queryset):
    queryset.favorite_count