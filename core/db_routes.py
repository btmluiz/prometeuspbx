class DbRouter:
    db_name = None
    models = []
    app_labels = []

    def db_for_read(self, model, **hints):
        if model.__name__ in self.get_models:
            return self.get_db_name(model.__name__)
        return None

    def db_for_write(self, model, **hints):
        if model.__name__ in self.get_models:
            return self.get_db_name(model.__name__)
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1.__str__() in self.get_models
            or obj1._meta.app_label in self.get_app_labels
        ) or (
            obj2.__str__() in self.get_models
            or obj2._meta.app_label in self.get_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db != self.get_db_name(model_name):
            return True

        if (model_name in self.get_models) or (app_label in self.get_app_labels):
            return True

        return False

    @property
    def get_models(self):
        return self.models

    @property
    def get_app_labels(self):
        return self.app_labels

    def get_db_name(self, model_label):
        return self.db_name
