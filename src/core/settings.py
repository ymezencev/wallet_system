from django.test.runner import DiscoverRunner


class NonInteractiveTestRunner(DiscoverRunner):
    """Не интерактивное тестирование. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interactive = False

    def teardown_databases(self, old_config, **kwargs):
        try:
            super().teardown_databases(old_config, **kwargs)
        except RuntimeError:
            pass
