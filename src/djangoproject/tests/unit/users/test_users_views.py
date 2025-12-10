from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from unittest.mock import patch


class BaseUserTestCase(APITestCase):
    def create_user_with_token(self, username="user", password="pass123"):
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return user, token


class UsersOperationsViewTests(BaseUserTestCase):
    def setUp(self):
        self.user, self.token = self.create_user_with_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_get_returns_authenticated_user_data(self):
        response = self.client.get("/user/ops")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.user.username)

    def test_patch_updates_user_fields(self):
        payload = {"first_name": "NewName"}

        response = self.client.patch("/user/ops", payload)

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "NewName")

    def test_patch_invalid_payload_returns_400(self):
        payload = {"username": ""}

        response = self.client.patch("/user/ops", payload)

        self.assertEqual(response.status_code, 400)

    def test_delete_removes_user_successfully(self):
        response = self.client.delete("/user/ops")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class CreateUserViewTests(APITestCase):
    def test_post_creates_user_successfully(self):
        # Fixed: Added required email field and stronger password
        payload = {
            "username": "newuser",
            "password": "StrongPass123!",  # Stronger password to pass Django validation
            "email": "newuser@example.com"
        }

        response = self.client.post("/user/create", payload)
    
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_post_invalid_data_returns_400(self):
        payload = {"username": ""}

        response = self.client.post("/user/create", payload)

        self.assertEqual(response.status_code, 400)


class ListAllUsersViewTests(BaseUserTestCase):
    def setUp(self):
        self.admin, self.admin_token = self.create_user_with_token("admin")
        self.admin.is_staff = True
        self.admin.save()

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

        User.objects.create_user(username="u1", password="123")
        User.objects.create_user(username="u2", password="123")

    def test_get_returns_all_users_for_admin(self):
        response = self.client.get("/search")

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 3)


class ToggleFollowUserViewTests(BaseUserTestCase):
    def setUp(self):
        self.user, self.token = self.create_user_with_token("alice")
        self.target, _ = self.create_user_with_token("bob")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    @patch("users.service.toggle_user_follow")
    def test_patch_calls_service_and_returns_message(self, mock_service):
        payload = {"target_username": self.target.username}

        response = self.client.patch("/follow-toggle", payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], f"The user {self.user.username} followed {self.target.username}")

    def test_patch_missing_username_returns_400(self):
        payload = {}

        response = self.client.patch("/follow-toggle", payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("target_username is required", response.data["error"])

    @patch("users.service.toggle_user_follow")
    def test_patch_service_validation_error_returns_400(self, mock_service):
        mock_service.side_effect = ValidationError("User does not exist")
        payload = {"target_username": "ghost"}

        response = self.client.patch("/follow-toggle", payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn('[ErrorDetail(string="User \'ghost\' not found.", code=\'invalid\')]', str(response.data["error"]))

    # Fixed: Patch the import location in the views module, not the service module
    @patch("users.views.toggle_user_follow")
    def test_patch_unexpected_error_returns_500(self, mock_service):
        mock_service.side_effect = Exception("Unexpected")

        payload = {"target_username": self.target.username}

        response = self.client.patch("/follow-toggle", payload)

        self.assertEqual(response.status_code, 500)
        self.assertIn("unexpected server error", response.data["error"].lower())