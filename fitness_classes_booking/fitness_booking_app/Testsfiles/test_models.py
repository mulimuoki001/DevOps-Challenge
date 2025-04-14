from datetime import date, time


from django.core.exceptions import ValidationError
from django.test import TestCase
from fitness_booking_app.models import Booking, CustomUser, FitnessClasses


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123",
            phone_number="1234567890",
            membership_type="GOLD",
        )

    def test_user_creation(self):
        """Test that a CustomUser instance is created correctly."""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.phone_number, "1234567890")
        self.assertEqual(self.user.membership_type, "GOLD")
        self.assertTrue(self.user.check_password("securepassword123"))

    def test_unique_username_constraint(self):
        """Test that duplicate usernames are not allowed."""
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                username="testuser",
                email="newemail@example.com",
                password="anotherpassword",
            )

    def test_unique_phone_number(self):
        """Test that the phone number field enforces uniqueness."""
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                username="newuser",
                phone_number="1234567890",  # Same as existing user
                password="password123",
            )


class FitnessClassesModelTest(TestCase):
    def setUp(self):
        self.fitness_class = FitnessClasses.objects.create(
            class_name="Yoga Class",
            start_time=time(10, 0),
            end_time=time(11, 0),
            date=date.today(),
            instructor_name="John Doe",
            capacity=20,
        )

    def test_fitness_class_creation(self):
        """Test that a FitnessClasses instance is created correctly."""
        self.assertEqual(self.fitness_class.class_name, "Yoga Class")
        self.assertEqual(self.fitness_class.instructor_name, "John Doe")
        self.assertEqual(self.fitness_class.capacity, 20)

    def test_fitness_class_string_representation(self):
        """Test the string representation of a FitnessClasses instance."""
        expected_string = (
            f"Yoga Class - {self.fitness_class.date.strftime('%Y-%m-%d')} 10:00"
        )
        self.assertEqual(str(self.fitness_class), expected_string)


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="booker",
            password="password123",
        )
        self.fitness_class = FitnessClasses.objects.create(
            class_name="Pilates Class",
            start_time=time(14, 0),
            end_time=time(15, 0),
            date=date.today(),
            instructor_name="Jane Smith",
            capacity=15,
        )
        self.booking = Booking.objects.create(
            user=self.user,
            fitness_class=self.fitness_class,
            start_time=self.fitness_class.start_time,
            end_time=self.fitness_class.end_time,
        )

    def test_booking_creation(self):
        """Test that a Booking instance is created correctly."""
        self.assertEqual(self.booking.user.username, "booker")
        self.assertEqual(self.booking.fitness_class.class_name, "Pilates Class")
        self.assertEqual(self.booking.start_time, time(14, 0))
        self.assertEqual(self.booking.end_time, time(15, 0))

    def test_booking_string_representation(self):
        """Test the string representation of a Booking instance."""
        expected_string = f"{self.booking.user.username} booked {self.booking.fitness_class.class_name} on {self.booking.booked_at}"
        self.assertEqual(str(self.booking), expected_string)

    def test_booking_cannot_exceed_capacity(self):
        for _ in range(self.fitness_class.capacity - 1):
            Booking.objects.create(
                user=CustomUser.objects.create_user(
                    username=f"extrauser{_}", password="pass123"
                ),
                fitness_class=self.fitness_class,
                start_time=self.fitness_class.start_time,
                end_time=self.fitness_class.end_time,
            )
        with self.assertRaisesMessage(ValidationError, "Class is full"):
            Booking.objects.create(
                user=CustomUser.objects.create_user(
                    username="extrauser", password="pass123"
                ),
                fitness_class=self.fitness_class,
                start_time=self.fitness_class.start_time,
                end_time=self.fitness_class.end_time,
            )
