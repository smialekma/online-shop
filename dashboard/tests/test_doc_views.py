from django.urls import reverse

from django.test import RequestFactory, TestCase

from dashboard.views.doc_views import StaticPageView


class StaticPageViewTest(TestCase):

    def test_context_contains_page_name(self):
        request = RequestFactory().get("/")
        view = StaticPageView()
        view.page_name = "Test Page"
        view.request = request

        context = view.get_context_data()

        self.assertEqual(context["name"], "Test Page")

    def test_static_pages_context(self):
        pages = [
            ("terms-view", "Terms & Conditions"),
            ("about-view", "About Us"),
            ("contact-view", "Contact Us"),
            ("policy-view", "Privacy Policy"),
            ("returns-view", "Orders & Returns"),
            ("help-view", "Help"),
        ]

        for url_name, expected_name in pages:
            with self.subTest(page=url_name):
                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "dashboard/terms.html")
                self.assertEqual(response.context["name"], expected_name)
