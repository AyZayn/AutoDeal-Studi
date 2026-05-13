from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class TestUserModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123",
            first_name="Jean",
            last_name="Dupont",
            phone="0612345678",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@test.com")
        self.assertEqual(self.user.first_name, "Jean")

    def test_user_str(self):
        self.assertEqual(str(self.user), "Jean Dupont (test@test.com)")

    def test_user_default_role(self):
        self.assertEqual(self.user.role, "client")

    def test_user_password_hashed(self):
        self.assertNotEqual(self.user.password, "testpass123")
        self.assertTrue(self.user.check_password("testpass123"))


class TestRegisterAPI(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_success(self):
        data = {
            "username": "newuser",
            "email": "new@test.com",
            "password": "newpass123",
            "first_name": "Marie",
            "last_name": "Martin",
            "phone": "0611111111",
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_missing_fields(self):
        data = {"username": "newuser"}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        User.objects.create_user(username="existing", password="pass123", email="ex@test.com")
        data = {
            "username": "existing",
            "email": "other@test.com",
            "password": "pass123",
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestProfileAPI(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="profileuser",
            email="profile@test.com",
            password="pass123",
        )

    def test_profile_without_auth(self):
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "profileuser")

    def test_update_profile(self):
        self.client.force_authenticate(user=self.user)
        data = {"first_name": "Pierre", "city": "Paris"}
        response = self.client.patch("/api/profile/update/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Pierre")
        