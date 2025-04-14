from datetime import date, time

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from fitness_booking_app.models import Booking, FitnessClasses

User = get_user_model()


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.fitness_class = FitnessClasses.objects.create(
            class_name="Yoga Class",
            start_time=time(10, 0),
            end_time=time(11, 0),
            date=date.today(),
            instructor_name="John Doe",
            capacity=5,
        )

    def test_register_view(self):
        """Test that user registration works correctly"""
        response = self.client.post(
            reverse("fitness_booking_app:register"),
            {
                "username": "newuser",
                "password1": "testpassword123",
                "password2": "testpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_add_class_view(self):
        """Test that an admin can add a fitness class"""
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(
            reverse("fitness_booking_app:add-class"),
            {
                "class_name": "Pilates",
                "start_time": "12:00",
                "end_time": "13:00",
                "date": date.today(),
                "instructor_name": "Jane Doe",
                "capacity": 10,
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        """Test that logging out redirects to login page"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("fitness_booking_app:logout"))
        self.assertEqual(response.status_code, 302)

    def test_index_view(self):
        """Test that the index page loads successfully"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("fitness_booking_app:index"))
        self.assertEqual(response.status_code, 200)

    def test_book_class_view(self):
        """Test that a user can book a class"""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("fitness_booking_app:book_class", args=[self.fitness_class.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Booking.objects.filter(
                user=self.user, fitness_class=self.fitness_class
            ).exists()
        )

    def test_book_full_class(self):
        """Test that a full class cannot be booked"""
        self.fitness_class.capacity = 0
        self.fitness_class.save()
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("fitness_booking_app:book_class", args=[self.fitness_class.id]),
            follow=True,
        )
        self.assertContains(response, "Class is full")

    def test_duplicate_booking(self):
        """Test that a user cannot book the same class twice"""
        self.client.login(username="testuser", password="password123")
        Booking.objects.create(
            user=self.user,
            fitness_class=self.fitness_class,
            start_time=self.fitness_class.start_time,
            end_time=self.fitness_class.end_time,
        )
        response = self.client.post(
            reverse("fitness_booking_app:book_class", args=[self.fitness_class.id])
        )
        self.assertRedirects(response, reverse("fitness_booking_app:index"))

    def test_bookings_view(self):
        """Test that the bookings page loads for logged-in users"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("fitness_booking_app:bookings"))
        self.assertEqual(response.status_code, 200)
