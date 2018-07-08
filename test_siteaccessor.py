from unittest import TestCase
from .siteaccessor import SiteAccessor


class TestSiteAccessor(TestCase):
    def setUp(self):
        self.site_accessor = SiteAccessor()

    def tearDown(self):
        del self.site_accessor

    def test_count(self):
        self.site_accessor.count = 123
        self.assertEqual(123, self.site_accessor.count)
