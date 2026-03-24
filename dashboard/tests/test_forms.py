from django.test import TestCase

from dashboard.forms import SearchForm


class SearchFormTests(TestCase):

    def test_form_valid(self):
        form = SearchForm(data={"query": "laptop"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "laptop")

    def test_query_required(self):
        form = SearchForm(data={"query": ""})

        self.assertFalse(form.is_valid())
        self.assertIn("query", form.errors)

    def test_query_max_length(self):
        form = SearchForm(data={"query": "a" * 300})

        self.assertFalse(form.is_valid())
        self.assertIn("query", form.errors)
