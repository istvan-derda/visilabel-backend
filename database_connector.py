import psycopg2


class DAO:
    def __init__(self, database_url):
        self.conn = psycopg2.connect(database_url, sslmode='require')

    def __del__(self):
        self.conn.close()

    def get_all_design_ids(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                    SELECT *
                    FROM designs
                """
            )
            return cursor.fetchall()

    def write_rating(self, user_id, design_id, background_color, rating):
        with self.conn.cursor() as cursor:
            SQL = """
                INSERT INTO rated_configurations (user_id, design_id, background_color, rating, impl_id)
                VALUES (%s, %s, %s, %s, %s)
                """
            data = (user_id, design_id, background_color, rating, 1)
            cursor.execute(SQL, data)
            self.conn.commit()
