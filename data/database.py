import sqlite3
from uuid import uuid4
from domain.post import Post


class Database:

    def __init__(self, database_name: str) -> None:
        self.db_name = database_name
        self.users_table = "users"
        self.posts_table = "posts"
        self.comments_table = "comments"
        self.id_delimiter = ":"

    def setup(self):
        self.__execute("PRAGMA foreign_keys = ON")
        self.__create_tables()

    # ===== POSTS =====
    def save_post(self, post: Post):
        print(post)
        return self.__save_row(self.posts_table, post)

    def get_posts(self):
        return self.__fetch_all(self.posts_table)

    def get_post(self, id):
        return self.__get_row_by_field(id, self.posts_table, "id")

    # ===== USERS =====
    def get_users(self):
        return self.__fetch_all(self.users_table)

    def get_user(self, id):
        return self.__get_row_by_field(id, self.users_table, "id")

    def save_user(self, user):
        return self.__save_row(self.users_table, user)

    # ===== COMMENTS =====
    def save_comment(self, comment):
        return self.__save_row(self.comments_table, comment)

    def get_comments_for_post(self, id):
        get_sql = f"""SELECT * FROM {self.comments_table} WHERE post_id=?"""
        return self.__execute_with_values(get_sql, (id,))

    def __create_tables(self):

        users_sql = f"""CREATE TABLE IF NOT EXISTS {self.users_table}(
            id TEXT PRIMARY KEY NOT NULL,
            trail_name TEXT NOT NULL,
            bio TEXT NOT NULL
        )
        """

        posts_sql = f"""CREATE TABLE IF NOT EXISTS {self.posts_table}(
            id TEXT PRIMARY KEY NOT NULL,
            created_at TEXT NOT NULL,
            user_id TEXT,
            title TEXT NOT NULL,
            text TEXT NOT NULL
        )
        """

        comments_sql = f"""CREATE TABLE IF NOT EXISTS {self.comments_table}(
            id TEXT PRIMARY KEY NOT NULL,
            created_at TEXT NOT NULL,
            user_id TEXT NOT NULL,
            post_id TEXT NOT NULL,
            text TEXT NOT NULL
        )
        """

        self.__execute(users_sql)
        self.__execute(posts_sql)
        self.__execute(comments_sql)

    def __get_row_by_field(self, id, table_name, field):
        sql = f"SELECT * FROM {table_name} WHERE {field}=?"
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id,))
            tup = cursor.fetchall()
            if len(tup) != 1:
                return []
            return tup[0]

    def __save_row(self, table_name, obj):

        items = obj.__dict__.items()

        values = ()
        values_holders = ""

        keys_str = ""
        for k, v in items:
            if k == "id":
                values += (f"{table_name}{self.id_delimiter}{str(uuid4())}",)
            else:
                values = values + (v,)
            keys_str += k + ","
            values_holders += "?,"

        keys_str = keys_str[:-1]
        values_holders = values_holders[:-1]

        insert_sql = f"""INSERT INTO {table_name}
                     ({keys_str}) 
                     VALUES({values_holders}) 
                     RETURNING *"""
        row = self.__execute_with_values(insert_sql, values)[0]
        return row

    def __fetch_all(self, table: str):
        sql = f"SELECT * FROM {table} WHERE 1"
        cursor = self.__execute(sql)
        return cursor.fetchall()

    def __execute(self, sql: str):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            return cursor

    def __execute_with_values(self, sql: str, values: tuple):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            rows = cursor.fetchall()
            conn.commit()
            return rows
