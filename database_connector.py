import psycopg2


# noinspection SqlNoDataSourceInspection
class DAO:
    def __init__(self, database_url):
        self.conn = psycopg2.connect(database_url)

    def __del__(self):
        self.conn.close()

    def get_design_ids(self, limit):
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT *
                    FROM designs
                    ORDER BY RANDOM()
                    LIMIT {limit}
                """
            )
            return cursor.fetchall()

    def get_batches_with_one_label(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            SELECT DISTINCT design_id 
            FROM (
                SELECT count(*) AS appeared_n_times, design_id, background_color 
                FROM rated_configurations 
                GROUP BY design_id, background_color
            ) AS rated_configurations_with_count
            WHERE appeared_n_times = 1
            ORDER BY RANDOM()
            LIMIT 100;""")
            design_ids = [row[0] for row in cursor.fetchmany(100)]
            batches = [self._get_batch_with_one_label(design_id) for design_id in design_ids]
            return batches

    def _get_batch_with_one_label(self, design_id):
        with self.conn.cursor() as cursor:
            cursor.execute(f"""
                SELECT background_color
                FROM (
                    SELECT count(*) AS appeared_n_times, design_id, background_color 
                    FROM rated_configurations 
                    GROUP BY design_id, background_color
                ) AS rated_configurations_with_count
                WHERE appeared_n_times = 1
                AND design_id = {design_id}
                LIMIT 8
            """)
            background_colors = [row[0] for row in cursor.fetchmany(8)]
            batch = {'design_id': design_id, 'background_colors': background_colors}
            return batch


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
