

# key, value 값으로부터 queryset filter
def get_filtered_queryset(queryset, key, value):
    if key == 'shape':
        return queryset.filter(shape__name=value)
    elif key == 'color':
        return queryset.filter(color__name=value)
    elif key == 'handle':
        return queryset.filter(handle__name=value)
    elif key == 'charm':
        return queryset.filter(charm__name=value)
    elif key == 'deco':
        return queryset.filter(deco__name=value)
    elif key == 'pattern':
        return queryset.filter(pattern__name=value)
    else:
        return queryset
