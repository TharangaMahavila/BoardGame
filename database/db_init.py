import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def init_database():
    try:
        # connect WITHOUT database first
        tmp_config = DB_CONFIG.copy()
        tmp_config.pop("database")

        conn = mysql.connector.connect(**tmp_config)
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")

        # Create tables if not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                game_id CHAR(8) PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                designer VARCHAR(80) NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                min_players TINYINT NOT NULL,
                max_players TINYINT NOT NULL,
                play_time_minutes SMALLINT NOT NULL,
                genre VARCHAR(80) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                street VARCHAR(80) NOT NULL,
                city VARCHAR(40) NOT NULL,
                postal_code VARCHAR(10) NOT NULL,
                phone_no VARCHAR(20) NOT NULL,
                email VARCHAR(80) UNIQUE,
                pwd_hash VARCHAR(200) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_no INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ship_street VARCHAR(80) NOT NULL,
                ship_city VARCHAR(40) NOT NULL,
                ship_postal_code VARCHAR(10) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_no INT NOT NULL,
                game_id CHAR(12) NOT NULL,
                quantity INT NOT NULL,
                line_total DECIMAL(10,2) NOT NULL,
                PRIMARY KEY (order_no, game_id),
                FOREIGN KEY (order_no) REFERENCES orders(order_no),
                FOREIGN KEY (game_id) REFERENCES games(game_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                user_id INT NOT NULL,
                game_id CHAR(12) NOT NULL,
                quantity INT NOT NULL,
                PRIMARY KEY (user_id, game_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (game_id) REFERENCES games(game_id)
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

        print("Database and tables ready")

    except Error as e:
        print("Database initialization error:", e)
