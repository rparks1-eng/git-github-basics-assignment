from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        self.assertEqual(resolve("/").func, home_page)

    def test_home_page_uses_home_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_has_minimum_content(self):
        response = self.client.get("/")
        self.assertContains(response, "To-Do Lists")
        self.assertContains(response, 'id="id_new_item"')
        self.assertContains(response, 'placeholder="Enter a to-do item"')
        self.assertContains(response, 'id="id_list_table"')
