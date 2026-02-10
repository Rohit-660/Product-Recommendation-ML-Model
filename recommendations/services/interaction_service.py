from django.db import connection
from datetime import datetime
from recommendations.services.redis_client import get_redis

def update_user_product_interactions():
    r = get_redis()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT last_processed_at
            FROM batch_metadata
            WHERE job_name = 'order_delta'
        """)
        last_ts = cursor.fetchone()[0]

        cursor.execute("""
            SELECT o.customer_id, oi.product_id, SUM(oi.qty_ordered) AS qty
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.id
            WHERE o.created_at > %s
            GROUP BY o.customer_id, oi.product_id
        """, [last_ts])

        rows = cursor.fetchall()

        for customer_id, product_id, qty in rows:
            score = qty * 5
            cursor.execute("""
                INSERT INTO user_product_interactions
                VALUES (%s,%s,%s,now())
                ON CONFLICT (user_id, product_id)
                DO UPDATE SET
                    interaction_score =
                    user_product_interactions.interaction_score + %s,
                    last_updated_at = now()
            """, [customer_id, product_id, score, score])

        cursor.execute("""
            UPDATE batch_metadata
            SET last_processed_at = %s
            WHERE job_name = 'order_delta'
        """, [datetime.utcnow()])

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                oi.product_id,
                SUM(oi.qty_ordered) AS total_qty
                FROM order_items oi
                JOIN orders o ON o.id = oi.order_id
                GROUP BY oi.product_id
                ORDER BY total_qty DESC
                LIMIT 50;
            """)

            global_rows = cursor.fetchall()

        r.set("global:top_products", ",".join(str(row[0]) for row in global_rows))
