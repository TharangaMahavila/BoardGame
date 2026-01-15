from database.db_connection import get_connection


class CartRepository:

    def save_item(self, user_id, game_id, qty):
        conn = get_connection()  # Get a database connection

        # SQL query to insert a new cart item
        sql = """
            INSERT INTO cart (
            user_id,
            game_id,
            quantity
            )
            VALUES (%s, %s, %s)
        """

        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    user_id,
                    game_id,
                    qty
                )
            )
            conn.commit()
            # Return number of rows affected
            return cursor.rowcount

    def get_by_user_id_and_game_id(self, user_id, game_id):
        conn = get_connection()  # Get a database connection

        # SQL query to fetch a specific cart item
        sql = """
            SELECT * FROM cart WHERE user_id=%s AND game_id=%s;
        """

        # Cursor returns results as a dictionary
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                sql,
                (
                    user_id,
                    game_id
                )
            )
            # Return a single matching record
            return cursor.fetchone()

    def update_item(self, user_id, game_id, qty):
        conn = get_connection()  # Get a database connection

        # SQL query to update the quantity of a cart item
        sql = """
            UPDATE cart SET quantity=%s WHERE user_id=%s AND game_id=%s;
        """

        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    qty,
                    user_id,
                    game_id
                )
            )
            conn.commit()
            # Return number of rows affected
            return cursor.rowcount

    def get_by_user_id(self, user_id):
        conn = get_connection()  # Get a database connection

        # SQL query to fetch all cart items for a user with game details
        sql = """
            SELECT c.game_id, g.title, g.unit_price, c.quantity FROM cart c
            JOIN games g ON g.game_id = c.game_id
            WHERE c.user_id = %s;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (user_id,))
            # Return all matching cart items
            return cursor.fetchall()
