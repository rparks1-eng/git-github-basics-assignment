"""A user's first visit to the To-Do Lists page."""

import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        self.browser = webdriver.Firefox(options=options)
        self.browser.set_page_load_timeout(15)
        self.addCleanup(self.browser.quit)

    def test_can_start_a_to_do_list(self):
        # A student visits the homepage to make a to-do list.
        self.browser.get(os.environ.get("TDD_URL", "http://127.0.0.1:8000"))
        # The page title and heading identify what the app does.
        self.assertIn("To-Do", self.browser.title)
        heading = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", heading)
        # An input invites the student to enter a task.
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a to-do item")
        # A list table is ready to show tasks.
        table = self.browser.find_element(By.ID, "id_list_table")
        self.assertEqual(table.tag_name, "table")


if __name__ == "__main__":
    unittest.main(verbosity=2)
