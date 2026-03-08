from django.test import TestCase, RequestFactory

from dashboard.views.errors import handler404, handler403, handler500


class ErrorHandlersTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_handler404(self):
        request = self.factory.get("/missing-page")

        response = handler404(request)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "dashboard/error.html")
        self.assertEqual(response.context["code"], "404")  # TODO
        self.assertEqual(response.context["title"], "Page not found")
        self.assertIn("doesn’t exist", response.context["description"])

    def test_handler403(self):
        request = self.factory.get("/forbidden")

        response = handler403(request)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "dashboard/error.html")
        self.assertEqual(response.context["code"], "403")
        self.assertEqual(response.context["title"], "Access denied")
        self.assertIn("permission", response.context["description"])

    def test_handler500(self):
        request = self.factory.get("/server-error")

        response = handler500(request)

        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, "dashboard/error.html")
        self.assertEqual(response.context["code"], "500")
        self.assertEqual(response.context["title"], "Server error")
        self.assertIn("unexpected error", response.context["description"])
