from datetime import datetime

from django.test import SimpleTestCase

from modules.expenses.serializers.CategorySerializer import CategorySerializer


class TestCategorySerializer(SimpleTestCase):

    def setUp(self):
        self.validData = {
            'name': 'Test Category',
            'details': 'Test Description',
            'status': 1,
            'created_at': datetime.now()
        }

        self.withoutName = {
            'details': 'Test Description',
            'status': 1,
            'created_at': datetime.now()
        }

        self.withOutStatus = {
            'name': 'Test Category',
            'details': 'Test Description',
            'created_at': datetime.now()
        }

        self.invalidStatusValue = {
            'name': 'Test Category',
            'details': 'Test Description',
            'status': 22,
            'created_at': datetime.now()
        }

    def test_valid_category_data(self):
        serializer = CategorySerializer(data=self.validData)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        # print("validation: ==== ", serializer.is_valid())
        # print("validation: ==== ", serializer.errors)
        # print("validation: ==== ", serializer.validated_data)
        self.assertEqual(serializer.validated_data['name'], 'Test Category')

    def test_name_is_required(self):
        serializer = CategorySerializer(data=self.withoutName)
        self.assertFalse(serializer.is_valid())
        # print(serializer.errors)
        self.assertIn("name", serializer.errors)

    def test_status_is_required(self):
        serializer = CategorySerializer(data=self.withOutStatus)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)

    def test_must_be_zero_or_one(self):
        serializer = CategorySerializer(data=self.invalidStatusValue)
        self.assertFalse(serializer.is_valid())
        # print("validation", serializer.errors)
        self.assertIn("status", serializer.errors)

