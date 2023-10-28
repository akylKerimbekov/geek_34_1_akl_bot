import sqlite3
from database import sql_queries


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3")
        self.cursor = self.connection.cursor()

    def sql_create_tables(self):
        if self.connection:
            print("Database connected successfully")

        self.connection.execute(sql_queries.CREATE_USER_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_RESULT_TABLE_QUERY)

    def sql_insert_user_query(self, telegram_id, username, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, username, first_name, last_name,)
        )
        self.connection.commit()

    def sql_insert_result_query(self, telegram_id, result):
        self.cursor.execute(
            sql_queries.INSERT_RESULT_QUERY,
            (None, telegram_id, result,)
        )
        self.connection.commit()

    def sql_select_result_query(self):
        return self.cursor.execute(
            sql_queries.SELECT_RESULT_QUERY,
        )
