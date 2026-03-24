from django.forms import model_to_dict
from django.test import TestCase

from customers.factories import CustomerFactory
from management_panel.forms import (
    NewsletterUpdateForm,
    OrderUpdateForm,
    PaymentUpdateForm,
    ProductUpdateForm,
    ReviewUpdateForm,
    SubscriberUpdateForm,
    UserUpdateForm,
)
from django import forms

from newsletter.factories import SubscriberFactory
from orders.factories import OrderFactory
from payments.factories import PaymentFactory
from product_reviews.factories import ReviewFactory
from products.factories import ProductFactory, BrandFactory, CategoryFactory


class NewsletterUpdateFormTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "title": "Test newsletter",
            "body": "Newsletter content",
            "created_at": "2024-01-01T12:00",
            "is_published": False,
            "to_publish": True,
        }

    def test_form_valid(self):
        form = NewsletterUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form = NewsletterUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        post = form.save()

        self.assertEqual(post.title, "Test newsletter")

    def test_created_at_widget(self):
        form = NewsletterUpdateForm()

        widget = form.fields["created_at"].widget

        self.assertIsInstance(widget, forms.DateInput)


class OrderUpdateFormTests(TestCase):

    def setUp(self):
        self.order = OrderFactory()
        self.valid_data = model_to_dict(self.order)

    def test_form_valid(self):
        form = OrderUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form = OrderUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        obj = form.save()

        self.assertEqual(obj.total_amount, self.order.total_amount)
        self.assertEqual(obj.email, self.order.email)

    def test_date_widgets(self):
        form = OrderUpdateForm()

        fields = [
            "date_ordered",
            "date_fulfilled",
            "created_at",
            "updated_at",
        ]

        for field in fields:
            widget = form.fields[field].widget
            self.assertIsInstance(widget, forms.DateInput)

    def test_all_model_fields_present(self):
        form = OrderUpdateForm()

        model_fields = {f.name for f in form._meta.model._meta.fields}

        form_fields = set(form.fields.keys())

        self.assertTrue(model_fields.issuperset(form_fields))


class PaymentUpdateFormTests(TestCase):

    def setUp(self):
        self.payment = PaymentFactory()
        self.valid_data = model_to_dict(self.payment)

    def test_form_valid(self):
        form = PaymentUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form = PaymentUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        obj = form.save()

        self.assertEqual(obj.stripe_checkout_id, self.payment.stripe_checkout_id)

    def test_created_at_widget(self):
        form = PaymentUpdateForm()

        widget = form.fields["created_at"].widget

        self.assertIsInstance(widget, forms.DateInput)

    def test_all_model_fields_present(self):
        form = PaymentUpdateForm()

        model_fields = {f.name for f in form._meta.model._meta.fields}

        form_fields = set(form.fields.keys())

        self.assertTrue(model_fields.issuperset(form_fields))


class ProductUpdateFormTests(TestCase):

    def setUp(self):
        self.product = ProductFactory.build(brand=BrandFactory.create(), category=CategoryFactory.create())
        self.valid_data = model_to_dict(self.product)

    def test_form_valid(self):
        form = ProductUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form = ProductUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        obj = form.save()

        self.assertEqual(obj.name, self.product.name)

    def test_date_added_widget(self):
        form = ProductUpdateForm()

        widget = form.fields["date_added"].widget

        self.assertIsInstance(widget, forms.DateInput)

    def test_all_model_fields_present(self):
        form = ProductUpdateForm()

        model_fields = {f.name for f in form._meta.model._meta.fields}

        form_fields = set(form.fields.keys())

        self.assertTrue(model_fields.issuperset(form_fields))


class ReviewUpdateFormTests(TestCase):

    def setUp(self):
        self.review = ReviewFactory()
        self.valid_data = model_to_dict(self.review)

    def test_form_valid(self):
        form = ReviewUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form = ReviewUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        obj = form.save()

        self.assertEqual(obj.title, self.review.title)

    def test_created_at_widget(self):
        form = ReviewUpdateForm()

        widget = form.fields["created_at"].widget

        self.assertIsInstance(widget, forms.DateInput)

    def test_all_model_fields_present(self):
        form = ReviewUpdateForm()

        model_fields = {f.name for f in form._meta.model._meta.fields}

        form_fields = set(form.fields.keys())

        self.assertTrue(model_fields.issuperset(form_fields))


class SubscriberUpdateFormTests(TestCase):

    def setUp(self):
        self.subscriber = SubscriberFactory.build()
        self.valid_data = model_to_dict(self.subscriber)

    def test_form_valid(self):
        form = SubscriberUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form = SubscriberUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        obj = form.save()

        self.assertEqual(obj.email, self.subscriber.email)

    def test_created_at_widget(self):
        form = SubscriberUpdateForm()

        widget = form.fields["date_subscribed"].widget

        self.assertIsInstance(widget, forms.DateTimeInput)

    def test_all_model_fields_present(self):
        form = SubscriberUpdateForm()

        model_fields = {f.name for f in form._meta.model._meta.fields}

        form_fields = set(form.fields.keys())

        self.assertTrue(model_fields.issuperset(form_fields))


class UserUpdateFormTests(TestCase):

    def setUp(self):
        self.user = CustomerFactory.build()
        self.valid_data = model_to_dict(self.user)

    def test_form_valid(self):
        form = UserUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form = UserUpdateForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

        obj = form.save()

        self.assertEqual(obj.username, self.user.username)

    def test_date_widgets(self):
        form = UserUpdateForm()

        fields = ["date_joined", "last_login"]

        for field in fields:
            widget = form.fields[field].widget
            self.assertIsInstance(widget, forms.DateTimeInput)

    def test_all_model_fields_present(self):
        form = UserUpdateForm()

        model_fields = {f.name for f in form._meta.model._meta.fields}
        model_fields.add("user_permissions")
        model_fields.add("groups")
        model_fields.remove("id")

        form_fields = set(form.fields.keys())

        self.assertTrue(model_fields.issuperset(form_fields))