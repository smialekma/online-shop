from django.test import TestCase, RequestFactory, override_settings

from customers.factories import CustomerFactory
from dashboard.views.errors import handler404, handler403, handler500


@override_settings(DEBUG=False)
class ErrorHandlersTests(TestCase):

    def setUp(self):
        self.user = CustomerFactory()
        self.client.force_login(self.user)

        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.request.session = self.client.session
        self.request.user = self.user

    def test_handler404(self):
        response = self.client.get("/non-existing-page/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "dashboard/error.html")
        self.assertEqual(response.context["code"], "404")
        self.assertEqual(response.context["title"], "Page not found")
        self.assertIn("doesn’t exist", response.context["description"])

    def test_handler403(self):

        response = handler403(self.request, exception=None)

        self.assertEqual(response.status_code, 403)
        self.assertIn("Access denied", response.content.decode())

    def test_handler500(self):
        response = handler500(self.request)

        self.assertEqual(response.status_code, 500)
        self.assertIn("Server error", response.content.decode())
