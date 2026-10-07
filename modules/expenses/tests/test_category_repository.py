from datetime import datetime

from django.test import TestCase


class TestCategoryRepository(TestCase):

    def test_repository_can_be_created(self):
        from modules.expenses.repositories import CategoryRepository
        repository = CategoryRepository()
        self.assertIsNotNone(repository)

    def test_repository_can_save_category(self):
        from modules.expenses.repositories import CategoryRepository
        repository = CategoryRepository()
        testData = {
            "name": "Category 1",
            "details": "Lorem ipsum",
            "status": 1,
            "created_at": datetime.now()
        }
        category = repository.create(data=testData)
        self.assertEqual(1, category)
