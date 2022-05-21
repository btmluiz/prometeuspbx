from core.db_routes import DbRouter


class SipRoutes(DbRouter):
    app_labels = ["pbx"]
    db_name = "asterisk"
