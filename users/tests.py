from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.token_url = reverse("token_obtain_pair")
        self.me_url = reverse("user_details")
        self.change_password_url = reverse("change_password")
        self.logout_url = reverse("logout")

        # Create test user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_user_registration(self):
        """Test user registration endpoint"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "password2": "newpassword123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtain(self):
        """Test token generation endpoint"""
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_details(self):
        """Test user details endpoint"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "test@example.com")

    def test_change_password(self):
        """Test change password endpoint"""
        self.client.force_authenticate(user=self.user)
        data = {"old_password": "testpass123", "new_password": "newpass456"}
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify password changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass456"))
