from database.db_connection import get_connection


class GameRepository:

    def get_all_genre(self):
        conn = get_connection()  # Get a database connection

        # SQL query to get all unique genres sorted alphabetically
        sql = """
            SELECT DISTINCT genre FROM games order by genre ASC;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            # Return all genres
            return cursor.fetchall()

    def get_genre_count(self, genre):
        conn = get_connection()  # Get a database connection

        # SQL query to count the number of games in a genre
        sql = """
            SELECT COUNT(genre) FROM games WHERE genre = %s;
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (genre,))
            # Return the count
            return cursor.fetchone()

    def get_designer_count(self, name):
        conn = get_connection()

        # SQL query to count games by designers starting with name
        sql = """
            SELECT COUNT(*) FROM games WHERE LOWER(designer) LIKE %s;
        """

        with conn.cursor() as cursor:
            # Execute with lowercase partial match
            cursor.execute(sql, (f"{name.lower()}%",))
            # Return the count
            return cursor.fetchone()

    def get_title_count(self, name):
        conn = get_connection()

        # SQL query to count games matching title as a whole word
        sql = """
            SELECT COUNT(*) FROM games WHERE LOWER(title) REGEXP %s;
        """

        # Regex pattern to match whole word in title
        pattern = rf'(^| ){name.lower()}( |$)'
        with conn.cursor() as cursor:
            cursor.execute(sql, (pattern,))
            # Return the count
            return cursor.fetchone()

    def find_paginated_by_genre(self, genre, limit, offset):
        conn = get_connection()

        # SQL query to fetch games by genre with pagination
        sql = """
            SELECT * FROM games WHERE genre = %s ORDER BY title ASC LIMIT %s OFFSET %s;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (genre, limit, offset))
            # Return list of games
            return cursor.fetchall()

    def find_paginated_by_designer(self, name, limit, offset):
        conn = get_connection()

        # SQL query to fetch games by designer with pagination
        sql = """
            SELECT * FROM games WHERE LOWER(designer) LIKE %s ORDER BY title ASC LIMIT %s OFFSET %s;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (f"{name.lower()}%", limit, offset))
            # Return list of games
            return cursor.fetchall()

    def find_paginated_by_title(self, name, limit, offset):
        conn = get_connection()

        # SQL query to fetch games by title with pagination
        sql = """
            SELECT * FROM games WHERE LOWER(title) REGEXP %s ORDER BY title ASC LIMIT %s OFFSET %s;
        """

        # Regex pattern to match title whole word
        pattern = rf'(^| ){name.lower()}( |$)'
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (pattern, limit, offset))
            # Return list of games
            return cursor.fetchall()

    def find_by_id(self, id):
        conn = get_connection()

        # SQL query to fetch a game by its ID
        sql = """
            SELECT * FROM games WHERE game_id = %s;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (id,))
            # Return single game record
            return cursor.fetchone()
