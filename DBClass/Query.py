import json
from typing import Union
from django.db import connection, connections
from helpers import DBHelper


class Query:
    def __init__(self, db_alias: str = 'default', has_transaction: int = 0):
        self.__connection = connections[db_alias]
        self.__mycursor = self.__connection.cursor()
        self.__has_transaction = has_transaction
        self.__query = ""
        self.__from_table = ""
        self.__selects = "SELECT *"
        self.__where_conditions = []
        self.__join_conditions = []
        self.__group_by = ""
        self.__order_by = ""
        self.__order_by_field = ""
        self.__query_order = ""
        self.__skip_rows = ""
        self.__query_limit = ""
        self.__cursor_paginate = 0

    def select(self, fields: list):
        """
        Constructs a SQL SELECT statement with the specified fields.

        Args:
            @param fields: Example:- ['table1.*', 'table2.column1', 'table3.column2', ....]
            @return: Returns an instance of the query builder for method chaining.
        """

        # self.__query += f"SELECT {', '.join(fields)}"
        self.__selects = f"SELECT {', '.join(fields)}"
        return self

    def table(self, table: str):
        """
        Specifies the table to be used in the SQL query.

        Args:
            @param table: The name of the table.
            @return: Returns an instance of the query builder for method chaining.
        """

        self.__from_table = table
        return self

    def where(self, column: str, operator: str, value: str, extra: str = None):
        """
        Adds a WHERE clause to the SQL query.

        Args:
            @param column: The column to apply the condition on.
            @param operator: The comparison operator (e.g., '=', '>', '<').
            @param value: The value to compare with.
            @param extra: For extra condition.
            @return: Returns an instance of the query builder for method chaining.
        """

        if len(self.__where_conditions) == 0:
            self.__where_conditions.append(f"{column} {operator} {value}")
            if extra is not None:
                self.__where_conditions.append(f"{extra}")
            return self

        if extra is not None:
            self.__where_conditions.append(f"AND ({extra})")
        else:
            self.__where_conditions.append(f"AND {column} {operator} {value}")

        return self

    def orWhere(self, column: str, operator: str, value: str):
        """
        Adds a OR clause to the SQL query.

        Args:
            @param column: The column to apply the condition on.
            @param operator: The comparison operator (e.g., '=', '>', '<').
            @param value: The value to compare with.
            @return: Returns an instance of the query builder for method chaining.
        """

        if len(self.__where_conditions) == 0:
            self.__where_conditions.append(f"{column} {operator} {value}")
            return self
        self.__where_conditions.append(f"OR {column} {operator} {value}")
        return self

    def whereBetween(self, column: str, condition: str):
        """
        Adds IN clause to the SQL query.

        Args:
            @param column: The column to apply the condition on.
            @param condition: A condition of values to include in the WHERE BETWEEN condition.
            @return: Returns an instance of the query builder for method chaining.
        """

        if len(self.__where_conditions) == 0:
            self.__where_conditions.append(f"{column} BETWEEN {condition}")
            return self
        self.__where_conditions.append(f"AND {column} BETWEEN {condition}")
        return self

    def whereIn(self, column: str, values: list):
        """
        Adds IN clause to the SQL query.

        Args:
            @param column: The column to apply the condition on.
            @param values: A list of values to include in the WHERE IN condition.
            @return: Returns an instance of the query builder for method chaining.
        """

        if len(self.__where_conditions) == 0:
            self.__where_conditions.append(f"{column} IN {tuple(values) if len(values) > 1 else f'({values[0]})'}")
            return self
        self.__where_conditions.append(f"AND {column} IN {tuple(values) if len(values) > 1 else f'({values[0]})'}")
        return self

    def whereNotIn(self, column: str, values: list):
        """
        Adds IN clause to the SQL query.

        Args:
            @param column: The column to apply the condition on.
            @param values: A list of values to include in the WHERE NOT IN condition.
            @return: Returns an instance of the query builder for method chaining.
        """

        if len(self.__where_conditions) == 0:
            self.__where_conditions.append(f"{column} NOT IN {tuple(values) if len(values) > 1 else f'({values[0]})'}")
            return self
        self.__where_conditions.append(f"AND {column} NOT IN {tuple(values) if len(values) > 1 else f'({values[0]})'}")
        return self

    def orWhereNotIn(self, column: str, values: list):
        """
        Adds IN clause to the SQL query.

        Args:
            @param column: The column to apply the condition on.
            @param values: A list of values to include in the OR WHERE NOT IN condition.
            @return: Returns an instance of the query builder for method chaining.
        """

        if len(self.__where_conditions) == 0:
            self.__where_conditions.append(f"{column} NOT IN {tuple(values) if len(values) > 1 else f'({values[0]})'}")
            return self
        self.__where_conditions.append(f"OR {column} NOT IN {tuple(values) if len(values) > 1 else f'({values[0]})'}")
        return self

    def leftJoin(self, table: str, condition: str):
        """
        Adds a LEFT JOIN clause to the SQL query.

        Args:
            @param table: The table to be joined.
            @param condition: The join condition (e.g., "table.column = parent_table.column").
            @return:Returns an instance of the query builder for method chaining.
        """

        self.__join_conditions.append(f"LEFT JOIN {table} ON {condition}")
        return self

    def rightJoin(self, table, condition):
        """
        Adds a RIGHT JOIN clause to the SQL query.

        Args:
            @param table: The table to be joined.
            @param condition: The join condition (e.g., "table.column = parent_table.column").
            @return:Returns an instance of the query builder for method chaining.
        """

        self.__join_conditions.append(f"RIGHT JOIN {table} ON {condition}")
        return self

    def innerJoin(self, table, condition):
        """
        Adds a INNER JOIN clause to the SQL query.

        Args:
            @param table: The table to be joined.
            @param condition: The join condition (e.g., "table.column = parent_table.column").
            @return:Returns an instance of the query builder for method chaining.
        """

        self.__join_conditions.append(f"INNER JOIN {table} ON {condition}")
        return self

    def fullOuterJoin(self, table: str, condition: str):
        """
        Adds a FULL OUTER JOIN clause to the SQL query.

        Args:
            @param table: The table to be joined.
            @type table: str
            @param condition: The join condition (e.g., "table.column = parent_table.column").
            @type condition: str
            @return:Returns an instance of the query builder for method chaining.
        """

        self.__join_conditions.append(f"FULL OUTER JOIN {table} ON {condition}")
        return self

    def groupBy(self, field: str):
        self.__group_by = f" GROUP BY {field}"
        return self

    def orderBy(self, field: str, order: str = "ASC"):
        """
        Adds an ORDER BY clause to the SQL query.

        Args:
            @param field: The field to order the results by.
            @type field: str
            @param order: The ordering direction, 'ASC' (default) or 'DESC'.
            @type order: (str, optional)
            @return:Returns an instance of the query builder for method chaining.
        """
        self.__order_by_field = field
        self.__query_order = order
        self.__order_by = f" ORDER BY {field} {order}"
        return self

    def skip(self, skip: int):
        """
        Adds an OFFSET clause to the SQL query.

        Args:
            @param skip: The maximum number of rows to skip.
            @type skip: int
            @return:Returns an instance of the query builder for method chaining.
        """

        self.__skip_rows = f" OFFSET {skip}"
        return self

    def limit(self, limit: int):
        """
        Adds an LIMIT clause to the SQL query.

        Args:
            @param limit: The maximum number of rows to return.
            @type limit: int
            @return:Returns an instance of the query builder for method chaining.
        """

        self.__query_limit = f" LIMIT {limit}"
        return self

    def build_query(self):
        query = self.__selects + " FROM " + self.__from_table

        if self.__join_conditions:
            query += " " + " ".join(self.__join_conditions)
        if self.__where_conditions:
            query += " WHERE " + " ".join(self.__where_conditions)
        if self.__group_by:
            query += self.__group_by
        if self.__order_by:
            query += self.__order_by
        if self.__query_limit:
            query += self.__query_limit
        if self.__skip_rows:
            query += self.__skip_rows

        return query

    def build(self):
        # print("con***", self.__where_conditions)
        # self.__query = self.__selects + " FROM " + self.__from_table
        #
        # if self.__join_conditions:
        #     self.__query += " " + " ".join(self.__join_conditions)
        # if self.__where_conditions:
        #     self.__query += " WHERE " + " ".join(self.__where_conditions)
        # if self.__order_by:
        #     self.__query += self.__order_by
        # if self.__query_limit:
        #     self.__query += self.__query_limit
        # if self.__skip_rows:
        #     self.__query += self.__skip_rows
        self.__query = self.build_query()
        print("query*****", self.__query)
        self.__mycursor.execute(self.__query)
        # return self.__query
        return self.__mycursor

    def getQuery(self):
        return self.build_query()

    def getAll(self):
        """
        Execute list of a dictionary object based on conditions, joins, orderby, limit etc.

        @return: dict: Ex. [{'column1': 'value1', 'column2': 'value2'}, {'column1': 'value1', 'column2': 'value2'}]

        Example:
           >>> example_1 = Query().table('your_table').leftJoin('table', 'table.column = your_table.column').where('column', '=', 'value').getAll()
           >>> example_2 = Query().table('your_table').leftJoin('table', 'table.column = your_table.column').where('column', 'like', f"'%value%'").getAll()
       """

        self.build()
        data = DBHelper.DictionaryFetchAll(self.__mycursor)
        # self.__mycursor.close()
        # self.__connection.close()
        # print(data)
        return data

    def first(self):
        """
        Get only single object based on condition

        @return: dict: Ex. {'column1': 'value1', 'column2': 'value2', 'column2': 'value3'}

        Example:
            >>> query_builder = Query().table('your_table').where('column', '=', 'value').first()
        """

        self.build()
        # query = self.__mycursor()
        data = DBHelper.DictionaryFetchOne(self.__mycursor)
        # self.__mycursor.close()
        # self.__connection.close()
        return data

    def __InsertQuery(self, data: Union[list, dict]):
        operator = ['%s']
        if type(data) == list:
            columns = ', '.join(data[0].keys())
            value_str = ','.join(operator * len(data[0].keys()))
            row_value = [tuple(list(item.values())) for item in data]
        else:
            columns = ', '.join(list(data.keys()))
            value_str = ','.join(operator * len(data.keys()))
            row_value = tuple(data.values())

        sql = "INSERT INTO " + self.__from_table + " (" + columns + ") VALUES (" + value_str + ")"
        # print("insert_query****", sql)

        if type(data) == list:
            self.__mycursor.executemany(sql.replace("'", ""), row_value)
        else:
            self.__mycursor.execute(sql, row_value)

        if self.__has_transaction == 0:
            self.__connection.commit()

        return self.__mycursor

    def insert(self, data: Union[list, dict]):
        """
        Executes an INSERT statement for a single record.

        Args:
            @param data: (dict, optional): A dictionary where keys are column names and values are the corresponding values to insert.
            @type data: dictionary

        @return: bool: Returns True if the insertion is successful, False otherwise.

        Example:
            >>> query_builder = Query()
            >>> record_to_insert = {'column1': 'value1', 'column2': 'value2'}
            >>> query_builder.table('your_table').insert(record_to_insert)

        """
        if len(data) == 0:
            return False
        self.__InsertQuery(data)
        if self.__has_transaction == 0:
            self.__connection.close()
        return True

    def insertGetID(self, data: dict):
        """
        Executes an INSERT statement for a single record and return inserted ID.

        Args:
            @param data: (dict, optional): A dictionary where keys are column names and values are the corresponding values to insert.
            @type data: dictionary

        @return: bool: Returns Inserted ID.

        Example:
            >>> query_builder = Query()
            >>> record_to_insert = {'column1': 'value1', 'column2': 'value2'}
            >>> query_builder.table('your_table').insert(record_to_insert)
        """

        if len(data) == 0:
            return False
        cursor = self.__InsertQuery(data)
        last_id = cursor.lastrowid
        return last_id

    def insertMany(self, data):
        """
        Executes a INSERT Statement for multiple records

        Args:
            @param data: A list of dictionary where every dictionary has keys are column names and values are the corresponding values to insert.
            @type data: List Of Dictionary

        @return: bool: Return True if the insert is successful, False otherwise.

        Example:
            >>> query_builder = Query()
            >>> records_to_insert = [
            ...     {'column1': 'value1', 'column2': 'value2'},
            ...     {'column1': 'value3', 'column2': 'value4'},
            ...     # Additional records...
            ... ]
            >>> query_builder.table('your_table').insertMany(records_to_insert)
        """
        # print("columns", data)
        # exit()
        if len(data) == 0:
            return False

        operator = ['%s']
        columns = ', '.join(data[0].keys())
        value_str = ','.join(operator * len(data[0].keys()))

        values_lists = [tuple(list(item.values())) for item in data]
        # print(values_lists)

        sql = "INSERT INTO " + self.__from_table + " (" + columns + ") VALUES (" + value_str + ")"
        self.__mycursor.executemany(sql.replace("'", ""), values_lists)
        if self.__has_transaction == 0:
            self.__connection.commit()
            self.__connection.close()
        return True

    def update(self, data: dict):
        """
        Executes a UPDATE statement based on the specified conditions

        Args:
            @param data: A dictionary where keys are column names and values are the corresponding values to update.
            @type data: dictionary

        @return: bool: Returns True if the update is successful, False otherwise.

        Example:
            >>> query_builder = Query().table('your_table').where('column1', '=', 'value1').update({'column1': 'value1', 'column2': 'value2'})
        """

        if len(data) == 0:
            return 'Syntax error or access violation: You have an error in your SQL syntax.'

        data_keys = list(data.keys())
        columns = ', '.join(key + '= %s' for key in data_keys)
        row_value = tuple(data.values())

        sql = "UPDATE " + self.__from_table + " SET " + columns + " WHERE " + " ".join(self.__where_conditions)
        print(sql)
        self.__mycursor.execute(sql, row_value)
        if self.__has_transaction == 0:
            self.__connection.commit()
            self.__connection.close()
        return True

    def delete(self):
        """
        Executes a DELETE statement based on the specified conditions

        @return: bool: Returns True if the deletion is successful, False otherwise.

        Example:
            >>> query_builder = Query().table('your_table').where('column1', '=', 'value1').delete()
        """

        sql = "DELETE FROM " + self.__from_table + " WHERE " + " ".join(self.__where_conditions)
        self.__mycursor.execute(sql)
        if self.__has_transaction == 0:
            self.__connection.commit()
            self.__connection.close()
        return True

    def executeRawQuery(self, query: str):
        """
        Executes Raw Query Statement

        @return: dict: Ex. [{'column1': 'value1', 'column2': 'value2'}, {'column1': 'value1', 'column2': 'value2'}]

        Example:
            >>> query_builder1 = Query().executeRawQuery('SELECT * FROM table')
            >>> query_builder2 = Query().executeRawQuery('SELECT * FROM table WHERE id > 1')
        """
        self.__query = query
        self.__mycursor.execute(self.__query)
        data = DBHelper.DictionaryFetchAll(self.__mycursor)
        return data

    def cursorPaginate(self, request, per_page: int = 5):
        if self.__order_by == '':
            raise RuntimeError('You must specify an orderBy clause when using this function.')

        query = self.__selects + " FROM " + self.__from_table
        decode_data = ''
        page = 1
        if self.__join_conditions:
            query += " " + " ".join(self.__join_conditions)
        dictionary_data = {}
        if request.query_params.get('cursor'):
            decode_data = DBHelper.DecodeData(request.query_params.get('cursor'))
            json_string = decode_data.replace("'", "\"").replace("True", "true").replace("False", "false")
            dictionary_data = json.loads(json_string)
            print("da", dictionary_data)

            # keys = dictionary_data.keys()
            # first_key, first_value = next(iter(dictionary_data.items()))
            # print("cursor", first_key.split("_")[])
            # exit()
            if dictionary_data['nextItems']:
                if self.__query_order == 'ASC' or self.__query_order == 'asc':
                    query += f" WHERE {self.__order_by_field} > '{dictionary_data['l-' + self.__order_by_field]}'"
                else:
                    query += f" WHERE {self.__order_by_field} < '{dictionary_data['f-' + self.__order_by_field]}'"
            else:
                if self.__query_order == 'ASC' or self.__query_order == 'asc':
                    query += f" WHERE {self.__order_by_field} >= '{dictionary_data['f-' + self.__order_by_field]}' AND id < '{dictionary_data['l-' + self.__order_by_field]}'"
                else:
                    query += f" WHERE {self.__order_by_field} <= '{dictionary_data['f-' + self.__order_by_field]}' AND id > '{dictionary_data['l-' + self.__order_by_field]}'"
            page = dictionary_data['page']

            # query += " WHERE " +
        if self.__where_conditions:
            query += " WHERE " + " ".join(self.__where_conditions)
        if self.__order_by:
            query += self.__order_by
        else:
            raise RuntimeError('You must specify an orderBy clause when using this function.')
        # 'You must specify an orderBy clause when using this function.'
        query += f" LIMIT {per_page}"

        # print("query*****", query)
        # print("request", request.META.get('HTTP_HOST'))
        self.__mycursor.execute(query)
        data = DBHelper.DictionaryFetchAll(self.__mycursor)
        self.__mycursor.close()
        self.__connection.close()
        path = request.META.get('HTTP_HOST') + request.META.get('PATH_INFO')
        # print("request*****", path)
        # print("data*****", data[-1])
        # print("order*****", self.__order_by_field)
        # get_field = self.__order_by.replace("DESC", "")
        first_row = data[0]
        last_row = ""
        prev_page_url = ""
        next_page_url = ""
        if len(data) > 0:
            last_row = data[-1]

        if len(data) == per_page:
            if page == 1:
                # next_link_dict = {f"f_{self.__order_by_field}": first_row[self.__order_by_field], f"l_{self.__order_by_field}": last_row[self.__order_by_field], 'nextItems': True, 'page': int(page + 1)}
                next_link_dict = {f"f-{self.__order_by_field}": first_row[self.__order_by_field],
                                  f"l-{self.__order_by_field}": last_row[self.__order_by_field], 'nextItems': True,
                                  'page': int(page + 1)}
                prev_page_url = ""
                print("link", next_link_dict)
                next_page_url = path + "?cursor=" + DBHelper.EncodeData(f"{next_link_dict}")
            else:
                # if request.query_params.get('cursor'):
                prev_page_no = page - 1
                next_page_no = page + 1
                # print("last_row", data)
                prev_link_dict = {f"f-{self.__order_by_field}": dictionary_data['f-' + self.__order_by_field],
                                  f"l-{self.__order_by_field}": first_row[self.__order_by_field], 'nextItems': False,
                                  'page': prev_page_no}
                next_link_dict = {f"f-{self.__order_by_field}": first_row[self.__order_by_field],
                                  f"l-{self.__order_by_field}": last_row[self.__order_by_field], 'nextItems': True,
                                  'page': next_page_no}
                prev_page_url = path + "?cursor=" + DBHelper.EncodeData(f"{prev_link_dict}")
                next_page_url = path + "?cursor=" + DBHelper.EncodeData(f"{next_link_dict}")
                print("quer", dictionary_data)
                print("pre", prev_link_dict)
                print("nex", next_link_dict)

        result = {
            'data': data,
            'path': path,
            'per_page': per_page,
            'next_page_url': next_page_url,
            'prev_page_url': prev_page_url,
            'decode': decode_data
        }
        return result

    def cursorPaginateV1(self, request, per_page: int = 5):
        if self.__order_by == '':
            raise RuntimeError('You must specify an orderBy clause when using this function.')

        query = self.__selects + " FROM " + self.__from_table
        decode_data = ''
        page = 1
        if self.__join_conditions:
            query += " " + " ".join(self.__join_conditions)
        dictionary_data = {}
        if request.query_params.get('cursor'):
            decode_data = DBHelper.DecodeData(request.query_params.get('cursor'))
            json_string = decode_data.replace("'", "\"").replace("True", "true").replace("False", "false")
            dictionary_data = json.loads(json_string)
            # print("da", dictionary_data)

            if dictionary_data['nextItems']:
                operator = "<"
                if self.__query_order == 'ASC' or self.__query_order == 'asc':
                    operator = ">"
                query += f" WHERE {self.__order_by_field} {operator} '{dictionary_data[self.__order_by_field]}'"
            else:
                if self.__query_order == 'ASC' or self.__query_order == 'asc':
                    query += f" WHERE {self.__order_by_field} < '{dictionary_data[self.__order_by_field]}'"

            page = dictionary_data['page']

            # query += " WHERE " +
        if self.__where_conditions:
            query += " WHERE " + " ".join(self.__where_conditions)

        if self.__order_by:
            if request.query_params.get('cursor'):
                if dictionary_data['nextItems']:
                    query += self.__order_by
                else:
                    query += f" ORDER BY {self.__order_by_field} DESC"
            else:
                query += self.__order_by
        else:
            raise RuntimeError('You must specify an orderBy clause when using this function.')

        # 'You must specify an orderBy clause when using this function.'
        query += f" LIMIT {per_page}"

        # print("query*****", query)
        # print("request", request.META.get('HTTP_HOST'))
        self.__mycursor.execute(query)
        data = DBHelper.DictionaryFetchAll(self.__mycursor)
        self.__mycursor.close()
        self.__connection.close()
        path = request.META.get('HTTP_HOST') + request.META.get('PATH_INFO')
        # print("request*****", path)
        # print("data*****", data[-1])
        # print("order*****", self.__order_by_field)
        # get_field = self.__order_by.replace("DESC", "")
        first_row = data[0]
        last_row = ""
        prev_page_url = ""
        next_page_url = ""
        if len(data) > 0:
            last_row = data[-1]

        if len(data) == per_page:
            if page == 1:
                next_link_dict = {f"{self.__order_by_field}": last_row[self.__order_by_field], 'nextItems': True,
                                  'page': int(page + 1)}

                if request.query_params.get('cursor'):
                    if not dictionary_data['nextItems']:
                        next_link_dict = {f"{self.__order_by_field}": first_row[self.__order_by_field],
                                          'nextItems': True,
                                          'page': int(page + 1)}
                prev_page_url = ""
                print("link", next_link_dict)
                next_page_url = path + "?cursor=" + DBHelper.EncodeData(f"{next_link_dict}")
            else:

                prev_page_no = page - 1
                next_page_no = page + 1
                prev_link_dict = {f"{self.__order_by_field}": first_row[self.__order_by_field], 'nextItems': False,
                                  'page': prev_page_no}
                next_link_dict = {f"{self.__order_by_field}": last_row[self.__order_by_field],
                                  'nextItems': True, 'page': next_page_no}
                if request.query_params.get('cursor'):
                    if not dictionary_data['nextItems']:
                        prev_link_dict = {f"{self.__order_by_field}": last_row[self.__order_by_field],
                                          'nextItems': False, 'page': prev_page_no}
                        next_link_dict = {f"{self.__order_by_field}": first_row[self.__order_by_field],
                                          'nextItems': True, 'page': next_page_no}
                prev_page_url = path + "?cursor=" + DBHelper.EncodeData(f"{prev_link_dict}")
                next_page_url = path + "?cursor=" + DBHelper.EncodeData(f"{next_link_dict}")
                # print("quer", dictionary_data)
                # print("pre", prev_link_dict)
                # print("nex", next_link_dict)

        result = {
            'data': data,
            'path': path,
            'per_page': per_page,
            'next_page_url': next_page_url,
            'prev_page_url': prev_page_url,
            # 'decode': decode_data
        }
        return result

    def beginTransaction(self):
        return self.__mycursor.execute('START TRANSACTION')
        # return self.__connection.start_transaction()
        # self.__connection.autocommit = False

    def commitTransaction(self):
        return self.__mycursor.execute('COMMIT')
        # return self.__connection.commit()

    def rollBack(self):
        return self.__mycursor.execute('ROLLBACK')
        # return self.__connection.rollback()

