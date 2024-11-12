import sqlite3


class Database:

    def __init__(self, database_name: str) -> None:
        self.db_name = database_name
        self.trail_angels_table = "trailangels"
        self.hikers_table = "hikers"
        self.posts_table = "posts"

    def setup(self):
        self.__execute("PRAGMA foreign_keys = ON")
        self.__create_tables()

    # ===== POSTS =====
    def save_post(self, post):
        row = self.__save_row(self.posts_table, post)
        return row

    def delete_post(self, post_id):
        sql = f"DELETE FROM {self.posts_table} WHERE id=?"
        self.__execute_with_values(sql, (post_id,))

    def get_posts(self):
        return self.__fetch_all(self.posts_table)

    def get_post(self, id):
        return self.__get_row_by_id(id, self.posts_table)

    # ===== HIKERS =====
    def get_hikers(self):
        return self.__fetch_all(self.hikers_table)

    def get_hiker(self, id):
        return self.__get_row_by_id(id, self.hikers_table)

    def save_hiker(self, hiker):
        return self.__save_row(self.hikers_table, hiker)

    # ===== TRAIL ANGELS =====

    def save_trail_angel(self, trail_angel):
        return self.__save_row(self.trail_angels_table, trail_angel)

    def get_trail_angels(self):
        return self.__fetch_all(self.trail_angels_table)

    def get_trail_angel(self, id):
        return self.__get_row_by_id(id, self.trail_angels_table)

    def __create_tables(self):
        trail_angels_sql = f"""CREATE TABLE IF NOT EXISTS {self.trail_angels_table}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            location TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            cost INTEGER NOT NULL
        )
        """

        hikers_sql = f"""CREATE TABLE IF NOT EXISTS {self.hikers_table}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trail_name TEXT NOT NULL,
            bio TEXT NOT NULL
        )
        """

        posts_sql = f"""CREATE TABLE IF NOT EXISTS {self.posts_table}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hiker_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            pickup TEXT NOT NULL,
            dropoff TEXT NOT NULL,
            date TEXT NOT NULL,
            num_passengers INTEGER,
            FOREIGN KEY(hiker_id) REFERENCES hikers(id)
        )
        """

        self.__execute(trail_angels_sql)
        self.__execute(hikers_sql)
        self.__execute(posts_sql)


    def __get_row_by_id(self, id, table_name):
        sql = f"SELECT * FROM {table_name} WHERE id={id}"
        cursor = self.__execute(sql)
        return cursor.fetchone()

    def __save_row(self, table_name, obj):

        items = obj.__dict__.items()

        values = ()
        values_holders = ""
        keys_str = ""
        for k, v in items:
            if (k != "id"):
                values = values + (v,)
                keys_str += k + ","
                values_holders += "?,"

        keys_str = keys_str[:-1]
        values_holders = values_holders[:-1]

        insert_sql = f"""INSERT INTO {table_name}({keys_str}) VALUES({values_holders}) RETURNING *"""
        row = self.__execute_with_values(insert_sql, values)
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
            row = cursor.fetchone()
            conn.commit()
            return row
