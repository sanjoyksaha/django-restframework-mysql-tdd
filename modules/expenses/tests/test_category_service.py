from datetime import datetime
from unicodedata import category
from unittest.mock import Mock

from django.test import TestCase

from modules.expenses.services import CategoryService


class TestCategoryService(TestCase):
    def setUp(self):
        self.repository = Mock()
        self.service = CategoryService(self.repository)

    def test_service_can_return_all_categories(self):
        categories = [{"id": 1, "name": "Food", "details": "Lorem ipsum"},
                      {"id": 2, "name": "Transport", "details": "Lorem ipsum dolar"}]

        self.repository.findAll.return_value = categories

        result = self.service.findAll(10, 1)
        self.assertEqual(result, categories)
        self.repository.findAll.assert_called_once_with(10, 1)

    def test_service_can_be_created(self):
        from modules.expenses.services import CategoryService

        service = CategoryService()

        self.assertIsNotNone(service)

    def test_service_can_be_created_with_repository(self):
        data = {
            "name": "Test Category",
            "details": "Lorem ipsum dolor sit amet",
            "status": 1,
            "created_at": datetime.now()
        }
        self.repository.create.return_value = 1

        category_id = self.service.create(data)
        self.assertEqual(category_id, 1)

        self.repository.create.assert_called_once_with(data=data)

    def test_service_can_find_category(self):
        data = {
            "id": 1,
            "name": "Test Category",
            "details": "Lorem ipsum dolor sit amet",
            "status": 1,
            "created_at": datetime.now()
        }

        self.repository.find.return_value = data

        result = self.service.find(1)
        self.assertEqual(result, data)
        self.repository.find.assert_called_once_with(1)

    def test_service_can_update_category(self):
        data = {
            "id": 1,
            "name": "Test Category",
            "details": "Lorem ipsum dolor sit amet",
            "status": 1
        }
        self.repository.update.return_value = 1

        result = self.service.update(1, data)
        self.assertEqual(result, 1)
        self.repository.update.assert_called_once_with(1, data=data)

    def test_service_can_delete_category(self):
        self.repository.delete.return_value = 1

        result = self.service.delete(1)
        self.assertEqual(result, 1)
        self.repository.delete.assert_called_once_with(1)
