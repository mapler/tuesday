from django.test import TestCase

# todo
from .models import ArmManager


class ArmKvsTestCase(TestCase):
    def setUp(self):
        self.manager = ArmManager()

    def test_arm_status_init(self):
        pass
        
    def test_arm_status(self):
        pass