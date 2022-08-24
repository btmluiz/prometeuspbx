class DbRouter:
    db_name = None
    app_labels = []

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.get_app_labels:
            return self.get_db_name(model._meta.app_label)
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.get_app_labels:
            return self.get_db_name(model._meta.app_label)
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.get_app_labels
            and obj2._meta.app_label in self.get_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.get_app_labels:
            if db != self.get_db_name(app_label):
                return False
        elif db == self.get_db_name(app_label):
            return False

        return True

    @property
    def get_app_labels(self):
        return self.app_labels

    def get_db_name(self, model_label):
        return self.db_name
