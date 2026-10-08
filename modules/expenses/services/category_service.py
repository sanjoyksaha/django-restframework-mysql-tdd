from config.settings import PER_PAGE
from modules.expenses.repositories import CategoryRepository


class CategoryService:
    def __init__(self, repository=None):
        self.repository = repository or CategoryRepository()

    def findAll(self, limit: int = PER_PAGE, page: int = 1):
        return self.repository.findAll(limit, page)

    def create(self, data: dict) -> int:
        return self.repository.create(data=data)

    def find(self, category_id: int):
        return self.repository.find(category_id)

    def update(self, category_id: int, data: dict):
        return self.repository.update(category_id, data=data)

    def delete(self, category_id: int):
        return self.repository.delete(category_id)
