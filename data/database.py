import sqlite3


class Database:

    def __init__(self, database_name: str) -> None:
        self.db_name = database_name
        self.trail_angels_table = "trailangels"
        self.hikers_table = "hikers"

    def setup(self):
        self.__create_tables()

    # ===== HIKERS =====
    def get_hikers(self):
        return self.__fetch_all(self.hikers_table)

    def save_hiker(self, hiker):

        values = (
            hiker.__dict__['trail_name'],
            hiker.__dict__['bio']
        )

        insert_sql = f"""INSERT INTO {self.hikers_table}(trail_name,bio) VALUES(?,?) RETURNING *"""
        row = self.__execute_with_values(insert_sql, values)
        return row

    # ===== TRAIL ANGELS =====

    def save_trail_angel(self, angel):

        values = (
            angel.__dict__['first_name'],
            angel.__dict__['last_name'],
            angel.__dict__['location'],
            angel.__dict__['capacity'],
            angel.__dict__['cost']
        )

        insert_sql = f"""INSERT INTO {self.trail_angels_table}(first_name,last_name,location,capacity,cost) VALUES(?,?,?,?,?) RETURNING *"""
        row = self.__execute_with_values(insert_sql, values)
        return row

    def get_trail_angels(self):
        return self.__fetch_all(self.trail_angels_table)

    def get_trail_angel(self, id):
        sql = f"SELECT * FROM {self.trail_angels_table} WHERE id={id}"
        cursor = self.__execute(sql)
        return cursor.fetchone()

    def __create_tables(self):
        trail_angel_sql = f"""CREATE TABLE IF NOT EXISTS {self.trail_angels_table}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            location TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            cost INTEGER NOT NULL
        )
        """

        hiker_sql = f"""CREATE TABLE IF NOT EXISTS {self.hikers_table}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trail_name TEXT NOT NULL,
            bio TEXT NOT NULL
        )
        """

        self.__execute(trail_angel_sql)
        self.__execute(hiker_sql)

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
