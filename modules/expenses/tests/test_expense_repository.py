from django.test import TestCase


class TestExpenseRepository(TestCase):

    def test_repository_can_be_created(self):
        from modules.expenses.repositories import ExpenseRepository
        repository = ExpenseRepository()
        self.assertIsNotNone(repository)