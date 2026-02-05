from django.db import connection
from datetime import datetime

def update_user_product_interactions():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT last_processed_at
            FROM batch_metadata
            WHERE job_name = 'order_delta'
        """)
        last_ts = cursor.fetchone()[0]

        cursor.execute("""
            SELECT o.customer_id, oi.product_id, SUM(oi.qty_ordered)
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.id
            WHERE o.created_at > %s
            GROUP BY o.customer_id, oi.product_id
        """, [last_ts])

        rows = cursor.fetchall()

        for user_id, product_id, qty in rows:
            score = qty * 5
            cursor.execute("""
                INSERT INTO user_product_interactions
                VALUES (%s,%s,%s,now())
                ON CONFLICT (user_id, product_id)
                DO UPDATE SET
                    interaction_score =
                    user_product_interactions.interaction_score + %s,
                    last_updated_at = now()
            """, [user_id, product_id, score, score])

        cursor.execute("""
            UPDATE batch_metadata
            SET last_processed_at = %s
            WHERE job_name = 'order_delta'
        """, [datetime.utcnow()])
