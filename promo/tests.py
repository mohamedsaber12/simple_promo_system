from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import NormalUserFactory, AdministratorUserFactory, PromoFactory, PromoUseFactory
from .models import Promo

# Create your tests here.


class TestPromoCreate(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.normal_user = NormalUserFactory(username="user1")
        self.normal_user.set_password("Awesome1")
        self.normal_user.save()

        self.administrator = AdministratorUserFactory(username="user2")
        self.administrator.set_password("Awesome2")
        self.administrator.save()

        self.promo_create_url = reverse("promo-list", )

    def test_create_promo_is_existing(self):
        response = self.client.post(self.promo_create_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_promo_with_no_auth(self):
        response = self.client.post(self.promo_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_promo_with_normal_user(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.post(self.promo_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_promo_with_admin_user_and_no_data(self):
        self.client.force_authenticate(self.administrator)
        response = self.client.post(self.promo_create_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_promo_success(self):
        promo_data = {
            "user": self.normal_user.id,
            "promo_type": "test type",
            "promo_code": "testpromocode",
            "start_date": "2020-11-05T19:00:00",
            "end_date": "2020-11-10T19:00:00",
            "promo_amount": 300,
            "is_active": True,
        }
        self.client.force_authenticate(self.administrator)
        response = self.client.post(self.promo_create_url, promo_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Promo.objects.all()), 1)


class TestPromoUpdate(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.normal_user = NormalUserFactory(username="user1")
        self.normal_user.set_password("Awesome1")
        self.normal_user.save()

        self.administrator = AdministratorUserFactory(username="user2")
        self.administrator.set_password("Awesome2")
        self.administrator.save()

        self.promo = PromoFactory()

        self.promo_update_url = reverse("promo-detail", args=[self.promo.pk])

    def test_update_promo_is_existing(self):
        response = self.client.patch(self.promo_update_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_promo_with_no_auth(self):
        response = self.client.patch(self.promo_update_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_promo_with_normal_user(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.patch(self.promo_update_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_promo_success(self):
        promo_data = {
            "promo_type": "test type edit",
            "is_active": False,
        }
        self.client.force_authenticate(self.administrator)
        response = self.client.patch(self.promo_update_url, promo_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.promo.refresh_from_db()
        self.assertEqual(self.promo.promo_type, "test type edit")
        self.assertEqual(self.promo.is_active, False)


class TestPromoDelete(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.normal_user = NormalUserFactory(username="user1")
        self.normal_user.set_password("Awesome1")
        self.normal_user.save()

        self.administrator = AdministratorUserFactory(username="user2")
        self.administrator.set_password("Awesome2")
        self.administrator.save()

        self.promo = PromoFactory()

        self.promo_delete_url = reverse("promo-detail", args=[self.promo.pk])

    def test_delete_promo_is_existing(self):
        response = self.client.delete(self.promo_delete_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_promo_with_no_auth(self):
        response = self.client.delete(self.promo_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_promo_with_normal_user(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.delete(self.promo_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_promo_success(self):

        self.client.force_authenticate(self.administrator)
        response = self.client.delete(self.promo_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Promo.objects.all()), 0)


class TestListPromoAdminUser(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.normal_user = NormalUserFactory(username="user1")
        self.normal_user2 = NormalUserFactory(username="user")
        self.normal_user.set_password("Awesome1")
        self.normal_user.save()

        self.administrator = AdministratorUserFactory(username="user2")
        self.administrator.set_password("Awesome2")
        self.administrator.save()

        self.promo = PromoFactory(user=self.normal_user)
        self.promo2 = PromoFactory(user=self.normal_user2)

        self.promo_list_url = reverse("promo-list")

    def test_lis_promos_is_existing(self):
        response = self.client.get(self.promo_list_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_lis_promos_with_no_auth(self):
        response = self.client.get(self.promo_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lis_promos_with_normal_user(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.get(self.promo_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lis_promos_success(self):
        self.client.force_authenticate(self.administrator)
        response = self.client.get(self.promo_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)


class TestMeListPromoNormalUser(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.normal_user = NormalUserFactory(username="user1")
        self.normal_user2 = NormalUserFactory(username="user")
        self.normal_user.set_password("Awesome1")
        self.normal_user.save()

        self.administrator = AdministratorUserFactory(username="user2")
        self.administrator.set_password("Awesome2")
        self.administrator.save()

        self.promo = PromoFactory(user=self.normal_user)
        self.promo2 = PromoFactory(user=self.normal_user2)

        self.promo_me_list_url = reverse("promo-me-list")

    def test_me_list_is_existing(self):
        response = self.client.get(self.promo_me_list_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_me_list_with_no_auth(self):
        response = self.client.get(self.promo_me_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_me_list_with_admin_user(self):
        self.client.force_authenticate(self.administrator)
        response = self.client.get(self.promo_me_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_me_list_success(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.get(self.promo_me_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)


class TestPromoPointsDetailView(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.normal_user = NormalUserFactory(username="user1")
        self.normal_user2 = NormalUserFactory(username="user")
        self.normal_user.set_password("Awesome1")
        self.normal_user.save()

        self.administrator = AdministratorUserFactory(username="user2")
        self.administrator.set_password("Awesome2")
        self.administrator.save()

        self.promo = PromoFactory(user=self.normal_user)

        self.promo_points_url = reverse("promo-points-detail",
                                        args=[self.promo.pk])

    def test_promo_points_is_existing(self):
        response = self.client.get(self.promo_points_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_promo_points_with_no_auth(self):
        response = self.client.get(self.promo_points_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_promo_points_with_admin_user(self):
        self.client.force_authenticate(self.administrator)
        response = self.client.get(self.promo_points_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_promo_points_with_normal_user_wrong_ownership(self):
        self.client.force_authenticate(self.normal_user2)
        response = self.client.get(self.promo_points_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_promo_points_with_normal_user_success(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.get(self.promo_points_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["remaining_points"])
        self.assertEqual(response.json()["remaining_points"],
                         self.promo.promo_amount)

    def test_promo_points_with_normal_user_success(self):
        self.promo.promo_amount = 200
        self.promo.save()
        PromoUseFactory(promo=self.promo, number_of_points=50)
        self.client.force_authenticate(self.normal_user)
        response = self.client.get(self.promo_points_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()["remaining_points"])
        self.assertEqual(response.json()["remaining_points"], 150.0)


class TestPromoPointsUse(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.normal_user = NormalUserFactory(username="user1")
        self.normal_user2 = NormalUserFactory(username="user")
        self.normal_user.set_password("Awesome1")
        self.normal_user.save()

        self.administrator = AdministratorUserFactory(username="user2")
        self.administrator.set_password("Awesome2")
        self.administrator.save()

        self.promo = PromoFactory(user=self.normal_user)

        self.promo_points_use_url = reverse("promo-points-use",
                                            args=[self.promo.pk])

    def test_promo_points_use_is_existing(self):
        response = self.client.post(self.promo_points_use_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_promo_points_use_with_no_auth(self):
        response = self.client.post(self.promo_points_use_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_promo_points_use_with_admin_user(self):
        self.client.force_authenticate(self.administrator)
        response = self.client.post(self.promo_points_use_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_promo_points_use_with_normal_user_wrong_ownership(self):
        self.client.force_authenticate(self.normal_user2)
        response = self.client.post(self.promo_points_use_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_promo_points_use_with_normal_user_without_payload(self):
        self.client.force_authenticate(self.normal_user)
        response = self.client.post(self.promo_points_use_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["points_to_use"][0],
                         "This field is required.")

    def test_promo_points_use_points_more_than_remaining(self):
        self.promo.promo_amount = 200
        self.promo.save()
        self.client.force_authenticate(self.normal_user)
        response = self.client.post(self.promo_points_use_url,
                                    {"points_to_use": 300})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["points_to_use"][0],
                         "remaining points is less than 300 it's 200.00")

    def test_promo_points_use_points_make_sure_that_remaining_points_decrease(
            self):
        self.promo.promo_amount = 320
        self.promo.save()
        self.client.force_authenticate(self.normal_user)
        response = self.client.post(self.promo_points_use_url,
                                    {"points_to_use": 300})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["remaining_points"], 20.0)
        self.promo.refresh_from_db()
        self.assertEqual(self.promo.remaining_points, 20.0)
