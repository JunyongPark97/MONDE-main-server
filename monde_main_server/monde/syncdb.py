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
import time


@transaction.atomic
def product_sync():
    for product in ProductMaster.objects.all():
        db_id = product.db_id
        c_product = CrawlerProduct.objects.get(pk=db_id)
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
            categories = product.categories
            colors = product.colors.colors
            ProductCategories.objects.update_or_create(product=p,
                                                       defaults={'shape_result': categories.shape_result,
                                                                 'type_result': categories.type_result,
                                                                 'charm_result': categories.charm_result,
                                                                 'deco_result': categories.deco_result,
                                                                 'pattern_result': categories.pattern_result,
                                                                 'colors': colors})
        except Exception as e:
            cause = str(e)
            DBProductSyncLogs.objects.create(db_product_id=db_id, cause=cause)


start = time.time()
product_sync()
print("time :", time.time()-start)
print('..1 ok')
