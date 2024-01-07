from django.apps import AppConfig



class UsersConfig(AppConfig):
    name = "zanhu.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import zanhu.users.signals  # noqa: F401
        except ImportError:
            pass
