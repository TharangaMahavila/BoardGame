from database.db_connection import get_connection


class OrderRepository:

    def save_order(self, user):
        conn = get_connection()
        cursor = conn.cursor()
        try:

            # Create the order record
            cursor.execute("""
                INSERT INTO orders (user_id, ship_street, ship_city, ship_postal_code)
                VALUES (%s, %s, %s, %s)
            """, (user["user_id"], user["street"], user["city"], user["postal_code"]))

            order_id = cursor.lastrowid

            # Create the order items records
            cursor.execute("""
                INSERT INTO order_items (order_no, game_id, quantity, line_total)
                SELECT %s, c.game_id, c.quantity, c.quantity * g.unit_price
                FROM cart c
                JOIN games g ON g.game_id = c.game_id
                WHERE c.user_id = %s
            """, (order_id, user["user_id"]))

            # Delete the cart records
            cursor.execute("""
                DELETE FROM cart WHERE user_id = %s
            """, (user["user_id"],))

            conn.commit()
            # Return the created order ID
            return order_id
        except Exception:
            conn.rollback()
            raise

    def get_order_by_user_id(self, user_id):
        conn = get_connection()

        # SQL query to get the most recent order for a user
        sql = """
            SELECT o.order_no, u.first_name, u.last_name, o.ship_street, o.ship_city, o.ship_postal_code, o.created FROM orders o
            JOIN users u ON u.user_id = o.user_id
            WHERE o.user_id = %s
            ORDER BY o.created DESC LIMIT 1;
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (user_id,))
            # Return single order record
            return cursor.fetchone()

    def get_order_items_by_order_id(self, order_id):
        conn = get_connection()

        # SQL query to get all items for a specific order
        sql = """
            SELECT oi.game_id, g.title, g.unit_price, oi.quantity, oi.line_total from order_items oi
            JOIN games g ON g.game_id = oi.game_id
            WHERE oi.order_no = %s
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (order_id,))
            # Return list of order items
            return cursor.fetchall()
