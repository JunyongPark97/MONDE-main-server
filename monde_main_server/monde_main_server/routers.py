

class MondeRouter(object):
    def __init__(self):
        self.model_list = ['web_crawler', 'default']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.model_list:
            return model._meta.app_label

        return 'default'

    def db_for_write(self, model, **hints):
        # print(model)
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # print(obj1, obj2)
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # print(app_label, db, model_name)
        if db == 'web_crawler':
            return False
        return True