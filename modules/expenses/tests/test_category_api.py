from unittest.mock import patch

from django.test import TestCase, Client
from rest_framework.test import APIClient

class TestCategoryApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.baseUrl = "/api/v1/expenses/categories"


    @patch('modules.expenses.views.category_views.CategoryService')
    def test_can_list_categories(self, mock_service):
        categories = [
            {"id": 1, "name": "Food", "details": "Food related expenses", "status": 1},
            {"id": 2, "name": "Investment", "details": "Investment related expenses", "status": 1},
            {"id": 3, "name": "Loan", "details": "Loan related expenses", "status": 1}
        ]

        mock_service.return_value.findAll.return_value = categories

        response = self.client.get(self.baseUrl)
        res = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['data'], categories)
        mock_service.return_value.findAll.assert_called_once()

    @patch('modules.expenses.views.category_views.CategoryService')
    def test_can_paginate_list_categories(self, mock_service):
        categories = [
            {"id": 1, "name": "Food", "details": "Food related expenses", "status": 1},
            {"id": 2, "name": "Investment", "details": "Investment related expenses", "status": 1},
            {"id": 3, "name": "Loan", "details": "Loan related expenses", "status": 1}
        ]

        mock_service.return_value.findAll.return_value = [categories[2]]
        response = self.client.get(self.baseUrl, {"limit": 2, "page": 2})

        res = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['data'], [categories[2]])
        mock_service.return_value.findAll.assert_called_once_with(limit=2, page=2)

    @patch('modules.expenses.views.category_views.CategoryService')
    def test_can_create_category(self, mock_service):
        mock_service.return_value.create.return_value = 1

        response = self.client.post(
            self.baseUrl,
            {
                "name": "Food",
                "details": "Food related expenses",
                "status": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

    @patch('modules.expenses.views.category_views.CategoryService')
    def test_can_get_category_details(self, mock_service):
        data = {
            "id": 1,
            "name": "Food",
            "details": "Food related expenses",
            "status": 1
        }
        mock_service.return_value.find.return_value = data

        response = self.client.get(
            f"{self.baseUrl}/1",
        )

        res = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['data'], data)
        mock_service.return_value.find.assert_called_once_with(1)

    @patch('modules.expenses.views.category_views.CategoryService')
    def test_return_404_when_category_does_not_exists(self, mock_service):
        mock_service.return_value.create.return_value = {}
        response = self.client.get(
            f"{self.baseUrl}/999",
        )
        res = response.json()
        self.assertEqual(response.status_code, 404)

    @patch("modules.expenses.views.category_views.CategoryService")
    def test_can_update_category(self, mock_service):
        mock_service.return_value.find.return_value = {
            "id": 1,
            "name": "Food",
            "details": "Old details",
            "status": 1,
        }
        mock_service.return_value.update.return_value = 1

        response = self.client.put(
            f"{self.baseUrl}/1",
            {
                "name": "Groceries",
                "details": "Updated details",
                "status": 1,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        mock_service.return_value.find.assert_called_once_with(1)
        mock_service.return_value.update.assert_called_once_with(
            1,
            {
                "name": "Groceries",
                "details": "Updated details",
                "status": 1,
            },
        )

    @patch("modules.expenses.views.category_views.CategoryService")
    def test_returns_404_when_updating_missing_category(self, mock_service):
        mock_service.return_value.find.return_value = {}

        response = self.client.put(
            f"{self.baseUrl}/999",
            {"name": "Groceries", "details": "Updated", "status": 1},
            format="json",
        )

        self.assertEqual(response.status_code, 404)
        mock_service.return_value.update.assert_not_called()

    @patch('modules.expenses.views.category_views.CategoryService')
    def test_can_delete_category(self, mock_service):
        mock_service.return_value.find.return_value = {
            "id": 1,
            "name": "Food",
            "details": "Old details",
            "status": 1,
        }
        mock_service.return_value.delete.return_value = 1

        response = self.client.delete(f"{self.baseUrl}/1")
        res = response.json()
        mock_service.return_value.find.assert_called_once_with(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['status'], 1)
        mock_service.return_value.delete.assert_called_once_with(1)

    @patch('modules.expenses.views.category_views.CategoryService')
    def test_returns_404_when_deleting_missing_category(self, mock_service):
        mock_service.return_value.find.return_value = {}
        response = self.client.delete(f"{self.baseUrl}/999")
        res = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(res['status'], 0)
        mock_service.return_value.delete.assert_not_called()