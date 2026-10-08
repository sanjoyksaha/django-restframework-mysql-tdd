from pygments.lexers import data

from DBClass.Query import Query
from config.settings import PER_PAGE


class CategoryRepository:
    __table = 'expense_categories'

    def __init__(self, db_alias='default'):
        self.db_alias = db_alias

    def findAll(self, limit: int = PER_PAGE, page: int = 1):
        return Query(self.db_alias).table(self.__table).limit(limit).skip((page - 1) * limit).getAll()

    def create(self, data: dict) -> int:
        return Query(self.db_alias).table(self.__table).insertGetID(data)

    def find(self, expense_id: int):
        return Query(self.db_alias).table(self.__table).where('id', '=', expense_id).first()

    def update(self, expense_id: int, data: dict):
        return Query(self.db_alias).table(self.__table).where("id", "=", expense_id).update(data)

    def delete(self, expense_id: int):
        return Query(self.db_alias).table(self.__table).where("id", "=", expense_id).delete()
