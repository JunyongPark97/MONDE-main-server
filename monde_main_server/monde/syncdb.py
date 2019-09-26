import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'monde_main_server.settings'
django.setup()

from logs.models import DBProductSyncLogs, DBProductImageSyncLogs, DBCategorySyncLogs, DBColorTabSyncLogs, \
    DBColorSyncLogs
from products.models import *
from monde.models import *


def get_on_sale(instance):
    for color_tab in instance.color_tabs.all():
        if not color_tab.on_sale:
            return False
    return True


def product_sync():
    for c_product in CrawlerProduct.objects.all():
        c_id = c_product.id
        c_price = c_product.price
        price = make_integer_price(c_price)
        on_sale = get_on_sale(c_product)
        try:
            Product.objects.update_or_create(db_id=c_id, defaults={'shopping_mall': c_product.shopping_mall,
                                                                   'name': c_product.product_name,
                                                                   'product_url': c_product.bag_url,
                                                                   'price': price,
                                                                   'is_on_sale': on_sale,
                                                                   'is_banned': c_product.is_banned,
                                                                   'crawler_created_at': c_product.crawled_date,
                                                                   'crawler_updated_at': c_product.updated_at})
        except Exception as e:
            cause = str(e)
            DBProductSyncLogs.objects.create(db_product_id=c_id, cause=cause)


def product_image_sync():
    for c_image in CrawlerBagimage.objects.all():
        c_id = c_image.id
        p_id = c_image.product.id
        product = Product.objects.get(db_id=p_id)
        try:
            ProductImage.objects.update_or_create(db_id=c_id, defaults={'image': c_image.bag_image,
                                                                        'origin_url': c_image.image_url,
                                                                        'order': c_image.order,
                                                                        'product': product})
        except Exception as e:
            cause = str(e)
            DBProductImageSyncLogs.objects.create(db_product_image_id=c_id, cause=cause)


def category_sync():
    for category in CategoryCategories.objects.all():
        ca_id = category.id
        c_product = category.bag_image.product
        product = Product.objects.get(db_id=c_product.id)
        try:
            ProductCategories.objects.update_or_create(db_id=ca_id, defaults={'shape_result': category.shape_result,
                                                                              'handle_result': category.handle_result,
                                                                              'color_result': category.color_result,
                                                                              'charm_result': category.charm_result,
                                                                              'deco_result': category.deco_result,
                                                                              'pattern_result': category.pattern_result,
                                                                              'product': product})
        except Exception as e:
            cause = str(e)
            DBCategorySyncLogs.objects.create(db_category_id=ca_id, cause=cause)


def color_tab_sync():
    for tab in CrawlerColortab.objects.all():
        t_id = tab.id
        t_product = tab.product
        product = Product.objects.get(db_id=t_product.id)
        try:
            ColorTab.objects.update_or_create(db_id=t_id, defaults={'color_tab_name': tab.colors,
                                                                    'product': product})
        except Exception as e:
            cause = str(e)
            DBColorTabSyncLogs.objects.create(db_colortab_id=t_id, cause=cause)


def color_sync():
    for color in CrawlerColortag.objects.all():
        co_id = color.id
        co_tab = color.colortab
        color_tab = ColorTab.objects.get(db_id=co_tab.id)
        try:
            Colors.objects.update_or_create(db_id=co_id, defaults={'color': color.color,
                                                                   'color_tab': color_tab})
        except Exception as e:
            cause = str(e)
            DBColorSyncLogs.objects.create(db_color_id=co_id, cause=cause)


# product_sync()
print('..1 ok')
# product_image_sync()
print('..2 ok')
# category_sync()
print('..3 ok')
# color_tab_sync()
print('..4 ok')
# color_sync()
print('..5 ok')
