from django.apps import AppConfig
from django.test import TestCase

from thema.apps import ThemaConfig


class TestThemaConfig(TestCase):
    def test_name(self):
        self.assertEqual(ThemaConfig.name, 'thema')
        self.assertTrue(issubclass(ThemaConfig, AppConfig))
