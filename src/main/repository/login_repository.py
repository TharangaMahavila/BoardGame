from database.db_connection import get_connection


class LoginRepository:

    def save_member(self, member):
        conn = get_connection()

        sql = """
            INSERT INTO users (
            first_name,
            last_name,
            street,
            city,
            postal_code,
            phone_no,
            email,
            pwd_hash
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    member.first_name,
                    member.last_name,
                    member.street,
                    member.city,
                    member.postal,
                    member.phone,
                    member.email,
                    member.password
                )
            )
            conn.commit()
            return cursor.lastrowid

    def get_member_by_email(self, email):
        conn = get_connection()

        sql = """
            SELECT * FROM users WHERE email = %s
        """

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (email,))
            return cursor.fetchone()
