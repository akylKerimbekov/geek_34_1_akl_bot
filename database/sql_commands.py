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
        self.connection.execute(sql_queries.CREATE_REFERENCE_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_NEWS_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_KEYWORD_TABLE_QUERY)
        self.connection.execute(sql_queries.CREATE_KEY_NEWS_TABLE_QUERY)
        try:
            self.connection.execute(sql_queries.ALTER_USER_TABLE)
        except sqlite3.OperationalError as e:
            pass
        self.sql_insert_key_word_query()


    def sql_insert_user_query(self, telegram_id, username, first_name, last_name):
        self.cursor.execute(
            sql_queries.INSERT_USER_QUERY,
            (None, telegram_id, username, first_name, last_name, None)
        )
        self.connection.commit()

    def sql_select_all_user_query(self):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "link": row[5],
        }
        return self.cursor.execute(
            sql_queries.SELECT_ALL_USER_QUERY,
        ).fetchall()

    def sql_select_user_query(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "link": row[5],
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_QUERY,
            (telegram_id,)
        ).fetchall()

    def sql_select_user_by_link_query(self, link):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "link": row[5],
        }
        return self.cursor.execute(
            sql_queries.SELECT_USER_BY_LINK_QUERY,
            (link,)
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
            (None, telegram_id, nickname, bio, age, occupation, photo,)
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

    def sql_select_all_referral_by_owner_query(self, owner_telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "owner_telegram_id": row[1],
            "referral_telegram_id": row[2],
        }
        return self.cursor.execute(
            sql_queries.SELECT_ALL_REFERRAL_BY_OWNER_QUERY,
            (owner_telegram_id,)
        ).fetchall()

    def sql_insert_like_query(self, owner_telegram_id, liker_telegram_id):
        self.cursor.execute(
            sql_queries.INSERT_LIKE_QUERY,
            (None, owner_telegram_id, liker_telegram_id,)
        )
        self.connection.commit()

    def sql_delete_user_form_query(self, owner_telegram_id):
        self.cursor.execute(
            sql_queries.DELETE_USER_FORM_QUERY,
            (owner_telegram_id,)
        )
        self.connection.commit()

    def sql_update_user_form_query(self, telegram_id, nickname, bio, age, occupation, photo):
        self.cursor.execute(
            sql_queries.UPDATE_USER_FORM_QUERY,
            (nickname, bio, age, occupation, photo, telegram_id,)
        )
        self.connection.commit()

    def sql_update_user_ref_query(self, reference_link, telegram_id):
        self.cursor.execute(
            sql_queries.UPDATE_USER_REF_QUERY,
            (reference_link, telegram_id,)
        )
        self.connection.commit()

    def sql_insert_referral_query(self, owner_telegram_id, referral_telegram_id):
        self.cursor.execute(
            sql_queries.INSERT_REFERRAL_QUERY,
            (None, owner_telegram_id, referral_telegram_id,)
        )
        self.connection.commit()

    def sql_insert_news_query(self, owner_telegram_id, title, href):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "owner_telegram_id": row[1],
            "title": row[2],
            "href": row[3],
            "is_favorite": row[4]
        }
        row = self.cursor.execute(
            sql_queries.INSERT_NEWS_QUERY,
            (None, owner_telegram_id, title, href, 0, )
        ).fetchone()
        self.connection.commit()
        return row

    def sql_update_fav_news_query(self, news_id):
        self.cursor.execute(
            sql_queries.UPDATE_FAV_NEWS_QUERY,
            (news_id,)
        )
        self.connection.commit()

    def sql_select_all_fav_news_query(self, owner_telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "owner_telegram_id": row[1],
            "title": row[2],
            "href": row[3],
            "is_favorite": row[4]
        }
        return self.cursor.execute(
            sql_queries.SELECT_ALL_FAV_NEWS_QUERY,
            (owner_telegram_id, )
        ).fetchall()

    def sql_insert_key_news_query(self, title, href):
        self.cursor.execute(
            sql_queries.INSERT_KEY_NEWS_QUERY,
            (None, title, href, )
        )
        self.connection.commit()

    def sql_insert_key_word_query(self):
        self.cursor.execute(
            sql_queries.INSERT_KEY_WORD_QUERY,
        )
        self.connection.commit()

    def sql_select_all_keyword_query(self):
        self.cursor.row_factory = lambda cursor, row: {
            "word": row[0],
        }
        return self.cursor.execute(
            sql_queries.SELECT_ALL_KEYWORD_QUERY,
        ).fetchall()

    def sql_select_top_5_key_news_query(self):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "title": row[1],
            "href": row[2],
        }
        return self.cursor.execute(
            sql_queries.SELECT_TOP_5_KEY_NEWS_QUERY,
        ).fetchall()