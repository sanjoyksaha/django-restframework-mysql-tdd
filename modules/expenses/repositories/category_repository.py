from pygments.lexers import data

from DBClass.Query import Query


class CategoryRepository:
    __table = 'expense_categories'

    def __init__(self, db_alias='default'):
        self.db_alias = db_alias

    def create(self, data: dict) -> int:
        return Query(self.db_alias).table(self.__table).insertGetID(data)

    def find(self, expense_id: int):
        return Query(self.db_alias).table(self.__table).where('id', '=', expense_id).first()

    def update(self, expense_id: int, data: dict):
        return Query(self.db_alias).table(self.__table).where("id", "=", expense_id).update(data)

    def delete(self, expense_id: int):
        return Query(self.db_alias).table(self.__table).where("id", "=", expense_id).delete()
