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

    def get_designer_count(self, name):
        conn = get_connection()

        sql = """
            SELECT COUNT(*) FROM games WHERE LOWER(designer) LIKE %s;
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (f"{name.lower()}%",))
            return cursor.fetchone()

    def get_title_count(self, name):
        conn = get_connection()

        sql = """
            SELECT COUNT(*) FROM games WHERE LOWER(title) REGEXP %s;
        """

        pattern = rf'(^| ){name.lower()}( |$)'
        with conn.cursor() as cursor:
            cursor.execute(sql, (pattern,))
            return cursor.fetchone()

    def find_paginated_by_genre(self, genre, limit, offset):
        conn = get_connection()

        sql = """
            SELECT * FROM games WHERE genre = %s ORDER BY title ASC LIMIT %s OFFSET %s;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (genre, limit, offset))
            return cursor.fetchall()

    def find_paginated_by_designer(self, name, limit, offset):
        conn = get_connection()

        sql = """
            SELECT * FROM games WHERE LOWER(designer) LIKE %s ORDER BY title ASC LIMIT %s OFFSET %s;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (f"{name.lower()}%", limit, offset))
            return cursor.fetchall()

    def find_paginated_by_title(self, name, limit, offset):
        conn = get_connection()

        sql = """
            SELECT * FROM games WHERE LOWER(title) REGEXP %s ORDER BY title ASC LIMIT %s OFFSET %s;
        """

        pattern = rf'(^| ){name.lower()}( |$)'
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (pattern, limit, offset))
            return cursor.fetchall()

    def find_by_id(self, id):
        conn = get_connection()

        sql = """
            SELECT * FROM games WHERE game_id = %s;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (id,))
            return cursor.fetchone()
