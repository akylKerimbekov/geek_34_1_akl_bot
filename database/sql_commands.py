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
        self.connection.execute(sql_queries.CREATE_BAN_USER_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_USER_FORM_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_LIKE_TABLE_QUERY)

    def sql_insert_user_query(self, telegram_id, username, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, username, first_name, last_name,)
        )
        self.connection.commit()

    def sql_select_all_user_query(self):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
        }
        return self.cursor.execute(
            sql_queries.SELECT_ALL_USER_QUERY,
        ).fetchall()

    def sql_insert_ban_user_query(self, telegram_id, username):
        self.cursor.execute(
            sql_queries.INSERT_BAN_USER_QUERY,
            (None, telegram_id, username, 1,)
        )
        self.connection.commit()

    def sql_insert_user_form_query(self, telegram_id, nickname, bio, age, occupation, photo):
        self.cursor.execute(
            sql_queries.INSERT_USER_FORM_QUERY,
            (None, telegram_id, nickname, bio, age, occupation, photo, )
        )
        self.connection.commit()

    def sql_select_user_form_query(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "nickname": row[2],
            "bio": row[3],
            "age": row[4],
            "occupation": row[5],
            "photo": row[6],
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_FORM_QUERY,
            (telegram_id,)
        ).fetchall()

    def sql_select_all_user_form_query(self):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "nickname": row[2],
            "bio": row[3],
            "age": row[4],
            "occupation": row[5],
            "photo": row[6],
        }
        return self.cursor.execute(
            sql_queries.SELECT_ALL_USER_FORM_QUERY,
        ).fetchall()

    def sql_insert_like_query(self, owner_telegram_id, liker_telegram_id):
        self.cursor.execute(
            sql_queries.INSERT_LIKE_QUERY,
            (None, owner_telegram_id, liker_telegram_id, )
        )
        self.connection.commit()

    def sql_delete_user_form_query(self, owner_telegram_id):
        self.cursor.execute(
            sql_queries.DELETE_USER_FORM_QUERY,
            (owner_telegram_id, )
        )
        self.connection.commit()

    def sql_update_user_form_query(self, telegram_id, nickname, bio, age, occupation, photo):
        self.cursor.execute(
            sql_queries.UPDATE_USER_FORM_QUERY,
            (nickname, bio, age, occupation, photo, telegram_id, )
        )
        self.connection.commit()