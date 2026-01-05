from database.db_connection import get_connection


class CartRepository:

    def save_item(self, user_id, game_id, qty):
        conn = get_connection()

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
            return cursor.rowcount

    def get_by_user_id_and_game_id(self, user_id, game_id):
        conn = get_connection()

        sql = """
            SELECT * FROM cart WHERE user_id=%s AND game_id=%s;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                sql,
                (
                    user_id,
                    game_id
                )
            )
            return cursor.fetchone()

    def update_item(self, user_id, game_id, qty):
        conn = get_connection()

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
            return cursor.rowcount
