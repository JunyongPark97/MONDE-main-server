from products.models import CategoryCategories


def get_tab_queryset(tab_no, queryset):
    categories_queryset = CategoryCategories.objects.all()

    if tab_no == 1:
        # 버킷백
        bucket_ids = get_bucket_list(categories_queryset)
        #TODO : 정렬시 정확도순으로 해야하나? 안해도 되면 정렬이 빨라짐
        # preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(bucket_ids)])
        bucket_products = queryset.filter(pk__in=bucket_ids)
        return bucket_products

    elif tab_no == 2:
        # 크로스백
        cross_ids = get_crossbag_list(categories_queryset)
        crossbag_products = queryset.filter(pk__in=cross_ids)
        return crossbag_products

    elif tab_no == 3:
        # 숄더백
        shoulder_ids = get_shoulder_list(categories_queryset)
        shoulder_products = queryset.filter(pk__in=shoulder_ids)
        return shoulder_products

    elif tab_no == 4:
        # 클러치백 & 미니백
        clutch_ids = get_clutch_list(categories_queryset)
        clutch_products = queryset.filter(pk__in=clutch_ids)
        return clutch_products

    elif tab_no == 5:
        # 토트백
        tote_ids = get_tote_list(categories_queryset)
        tote_products = queryset.filter(pk__in=tote_ids)
        return tote_products


def get_bucket_list(queryset):
    ids = []
    for instance in queryset:
        shape_data = instance.shape_result
        if not instance.bag_image:
            pass
        if 'bucket' in shape_data and shape_data['bucket'] > 0.5:
            ids.append(instance.bag_image.product.id)
            # ids[instance.bag_image.product.id] = shape_data['bucket']
    # sorted_bucket_list = sorted(ids, key=lambda kv: ids[kv], reverse=True)
    return ids


def get_crossbag_list(queryset):
    ids = []
    for instance in queryset:
        handle_data = instance.handle_result
        if not instance.bag_image:
            pass
        if 'shoulder' in handle_data and handle_data['shoulder'] > 0.4 or \
                'tote_shoulder' in handle_data and handle_data['tote_shoulder'] > 0.4:
            ids.append(instance.bag_image.product.id)
    return ids


def get_shoulder_list(queryset):
    ids = []
    for instance in queryset:
        handle_data = instance.handle_result
        if not instance.bag_image:
            pass
        if 'shoulder' in handle_data and handle_data['shoulder'] > 0.4 or \
                'tote_shoulder' in handle_data and handle_data['tote_shoulder'] > 0.4 or \
                'big_shoulder' in handle_data and handle_data['big_shoulder'] > 0.4:
            ids.append(instance.bag_image.product.id)
    return ids


def get_clutch_list(queryset):
    ids = []
    for instance in queryset:
        handle_data = instance.handle_result
        if not instance.bag_image:
            pass
        if 'clutch' in handle_data and handle_data['clutch'] > 0.5:
            ids.append(instance.bag_image.product.id)
    return ids


def get_tote_list(queryset):
    ids = []
    for instance in queryset:
        handle_data = instance.handle_result
        if not instance.bag_image:
            pass
        if 'tote' in handle_data and handle_data['tote'] > 0.4 or \
                'tote_shoulder' in handle_data and handle_data['tote_shoulder'] > 0.4:
            ids.append(instance.bag_image.product.id)
    return ids
