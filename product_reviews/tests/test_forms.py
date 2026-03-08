from django import forms
from django.forms import model_to_dict
from django.test import TestCase

from product_reviews.factories import ReviewFactory
from product_reviews.forms import ReviewForm
from product_reviews.models import Review


class ReviewFormTests(TestCase):

    def setUp(self):
        self.review = ReviewFactory()
        self.valid_data = model_to_dict(self.review)

    def test_form_valid(self):
        form = ReviewForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form = ReviewForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        obj = form.save()

        self.assertEqual(obj.title, self.review.title)

    def test_title_required(self):
        data = self.valid_data.copy()
        data["title"] = ""

        form = ReviewForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_rating_field_configuration(self):
        form = ReviewForm()

        field = form.fields["rating"]

        self.assertIsInstance(field, forms.ChoiceField)
        self.assertEqual(field.choices, Review.RATING_CHOICES)
        self.assertIsInstance(field.widget, forms.RadioSelect)

    def test_title_widget(self):
        form = ReviewForm()

        widget = form.fields["title"].widget

        self.assertIsInstance(widget, forms.TextInput)
        self.assertEqual(widget.attrs["class"], "input")
        self.assertEqual(widget.attrs["placeholder"], "Review title")

    def test_body_widget(self):
        form = ReviewForm()

        widget = form.fields["body"].widget

        self.assertIsInstance(widget, forms.Textarea)
        self.assertEqual(widget.attrs["class"], "input")
        self.assertEqual(widget.attrs["rows"], 3)

    def test_form_fields(self):
        form = ReviewForm()

        self.assertEqual(
            list(form.fields.keys()),
            ["title", "body", "rating"],
        )
