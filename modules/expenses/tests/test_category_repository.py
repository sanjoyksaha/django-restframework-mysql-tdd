from datetime import datetime

from django.test import TestCase

from modules.expenses.repositories import CategoryRepository


class TestCategoryRepository(TestCase):

    def setUp(self):
        self.repository = CategoryRepository()

    def test_repository_can_be_created(self):
        repository = CategoryRepository()
        self.assertIsNotNone(repository)

    def test_repository_can_save_category(self):
        testData = {
            "name": "Category 1",
            "details": "Lorem ipsum",
            "status": 1,
            "created_at": datetime.now()
        }
        category = self.repository.create(data=testData)
        self.assertIsNotNone(category)

    def test_repository_can_find_category(self):
        category_id = self.repository.create(data={
            "name": "Category 1",
            "details": "Lorem ipsum",
            "status": 1,
            "created_at": datetime.now()
        })

        category = self.repository.find(category_id)

        self.assertIsNotNone(category)
        self.assertEqual(category['id'], category_id)
        self.assertEqual(category['name'], 'Category 1')

    def test_repository_can_update_category(self):
        category_id = self.repository.create(data={
            "name": "Category 1",
            "details": "Lorem ipsum",
            "status": 1,
            "created_at": datetime.now()
        })

        update = self.repository.update(category_id, data={
            "name": "Category 2",
            "status": 0,
            "updated_at": datetime.now()
        })

        self.assertEqual(update, 1)

        category = self.repository.find(category_id)
        self.assertEqual(category['name'], 'Category 2')
        self.assertEqual(category['status'],0)

    def test_repository_can_delete_category(self):
        category_id = self.repository.create(data={
            "name": "Category 1",
            "details": "Lorem ipsum",
            "status": 1,
            "created_at": datetime.now()
        })

        delete = self.repository.delete(category_id)
        self.assertEqual(delete, 1)
        category = self.repository.find(category_id)
        self.assertEqual(category, {})