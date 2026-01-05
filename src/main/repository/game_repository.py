from database.db_connection import get_connection


class GameRepository:

    def get_all_genre(self):
        conn = get_connection()

        sql = """
            SELECT DISTINCT genre FROM games order by genre ASC;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_genre_count(self, genre):
        conn = get_connection()

        sql = """
            SELECT COUNT(genre) FROM games WHERE genre = %s;
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (genre,))
            return cursor.fetchone()

    def find_paginated(self, genre, limit, offset):
        conn = get_connection()

        sql = """
            SELECT * FROM games WHERE genre = %s ORDER BY title ASC LIMIT %s OFFSET %s;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (genre, limit, offset))
            return cursor.fetchall()

    def find_by_id(self, id):
        conn = get_connection()

        sql = """
            SELECT * FROM games WHERE game_id = %s;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (id,))
            return cursor.fetchone()
