from django.test import Client, TestCase
from django.urls import reverse


class URLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_url(self):
        response = self.client.get(reverse("fitness_booking_app:index"))
        self.assertEqual(response.status_code, 302)

    def test_add_class_url(self):
        response = self.client.get(reverse("fitness_booking_app:add-class"))
        self.assertIn(response.status_code, [200, 302])  # May require login

    def test_login_url(self):
        response = self.client.get(reverse("fitness_booking_app:login"))
        self.assertEqual(response.status_code, 200)

    def test_register_url(self):
        response = self.client.get(reverse("fitness_booking_app:register"))
        self.assertEqual(response.status_code, 200)

    def test_profile_url(self):
        response = self.client.get(reverse("fitness_booking_app:profile"))
        self.assertIn(response.status_code, [200, 302])  # May require login

    def test_logout_url(self):
        response = self.client.get(reverse("fitness_booking_app:logout"))
        self.assertEqual(response.status_code, 302)  # Redirects after logout

    def test_book_class_url(self):
        response = self.client.get(reverse("fitness_booking_app:book_class", args=[1]))
        self.assertIn(response.status_code, [200, 302])  # May require login

    def test_bookings_url(self):
        response = self.client.get(reverse("fitness_booking_app:bookings"))
        self.assertIn(response.status_code, [200, 302])  # May require login
