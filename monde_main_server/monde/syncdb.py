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
from mondebro.models import *
from monde.models import *
from django.db import transaction

#
# def get_on_sale(instance):
#     for color_tab in instance.color_tabs.all():
#         if not color_tab.on_sale:
#             return False
#     return True


@transaction.atomic
def product_sync():
    for product in ProductMaster.objects.all():
        db_id = product.db_id
        c_product = CrawlerProduct.objects.get(pk=db_id)
        print('--+==')
        try:
            p, _ = Product.objects.update_or_create(db_id=db_id,
                                                    defaults={'shopping_mall': product.shopping_mall,
                                                              'name': product.name,
                                                              'product_url': product.product_url,
                                                              'product_image_url': product.product_image_url,
                                                              'is_best': product.is_best,
                                                              'is_valid': product.is_valid,
                                                              'price': product.price,
                                                              'crawler_created_at': c_product.crawled_date,
                                                              'crawler_updated_at': c_product.updated_at})
            print(p)
            # categories = product.categories
            # colors = product.colors.colors
            # ProductCategories.objects.update_or_create(product=p,
            #                                            defaults={'shape_result': categories.shape_result,
            #                                                      'type_result': categories.type_result,
            #                                                      'charm_result': categories.charm_result,
            #                                                      'deco_result': categories.deco_result,
            #                                                      'pattern_result': categories.pattern_result,
            #                                                      'colors': colors})
        except Exception as e:
            cause = str(e)
            DBProductSyncLogs.objects.create(db_product_id=db_id, cause=cause)

#
# def category_sync():
#     for category in Categories.objects.all():
#         ca_id = category.id
#         c_product = category.bag_image.product
#         product = Product.objects.get(db_id=c_product.id)
#         try:
#             ProductCategories.objects.update_or_create(product=product, defaults={'shape_result': category.shape_result,
#                                                                               'handle_result': category.handle_result,
#                                                                               'color_result': category.color_result,
#                                                                               'charm_result': category.charm_result,
#                                                                               'deco_result': category.deco_result,
#                                                                               'pattern_result': category.pattern_result})
#         except Exception as e:
#             cause = str(e)
#             DBCategorySyncLogs.objects.create(db_category_id=ca_id, cause=cause)
#
#
# def color_tab_sync():
#     for tab in CrawlerColortab.objects.all():
#         t_id = tab.id
#         t_product = tab.product
#         product = Product.objects.get(db_id=t_product.id)
#         try:
#             ColorTab.objects.update_or_create(db_id=t_id, defaults={'color_tab_name': tab.colors,
#                                                                     'product': product})
#         except Exception as e:
#             cause = str(e)
#             DBColorTabSyncLogs.objects.create(db_colortab_id=t_id, cause=cause)
#
#
# def color_sync():
#     for color in CrawlerColortag.objects.all():
#         co_id = color.id
#         co_tab = color.colortab
#         color_tab = ColorTab.objects.get(db_id=co_tab.id)
#         try:
#             Colors.objects.update_or_create(db_id=co_id, defaults={'color': color.color,
#                                                                    'color_tab': color_tab})
#         except Exception as e:
#             cause = str(e)
#             DBColorSyncLogs.objects.create(db_color_id=co_id, cause=cause)


product_sync()
print('..1 ok')
# product_image_sync()
# print('..2 ok')
# category_sync()
# print('..3 ok')
# color_tab_sync()
# print('..4 ok')
# color_sync()
# print('..5 ok')
