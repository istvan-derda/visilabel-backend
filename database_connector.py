import psycopg2


# noinspection SqlNoDataSourceInspection
class DAO:
    def __init__(self, database_url):
        self.conn = psycopg2.connect(database_url)

    def __del__(self):
        self.conn.close()

    def get_100_design_ids(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                    SELECT *
                    FROM designs
                    ORDER BY RANDOM()
                    LIMIT 100
                """
            )
            return cursor.fetchall()

    def get_all_product_colors(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT * 
            FROM sprd_product_colors
            ORDER BY RANDOM()
            """)
            return cursor.fetchall()

    def write_rating(self, user_id, design_id, background_color, rating):
        with self.conn.cursor() as cursor:
            SQL = """
                INSERT INTO rated_configurations (user_id, design_id, background_color, rating, impl_id)
                VALUES (%s, %s, %s, %s, %s)
                """
            data = (user_id, design_id, background_color, rating, 5)
            result = cursor.execute(SQL, data)
            print(result)
            self.conn.commit()

    def get_rated_count(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT count(*)
                FROM rated_configurations
            """)
            return cursor.fetchall()

    def get_rated_count_for_user(self, user_id):
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
                    SELECT count(*)
                    FROM rated_configurations
                    where user_id = '{user_id}'
                """)
            return cursor.fetchall()
