
def make_integer_price(str_price):
    if '원' in str_price:
        str_price = str_price.split('원')[0]
    list_price = list(str_price)
    _temp = []
    for i in list_price:
        try:
            _temp.append(int(i))
        except:
            pass
    int_price = int(''.join(str(x) for x in _temp))
    return int_price