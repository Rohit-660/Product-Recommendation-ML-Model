import pandas as pd
import pickle
from mlxtend.frequent_patterns import fpgrowth, association_rules
from django.db import connection

BASKET_PATH = "recommendations/data/basket_rules.pkl"

def train_market_basket():

    with connection.cursor() as cursor:
        cursor.execute("""
             SELECT
                oi.order_id,
                oi.product_id
            FROM order_items oi
            JOIN orders o ON o.id = oi.order_id
        """)
        rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=["order_id", "product_id"])

    # df = pd.read_sql("""
    #     SELECT
    #         oi.order_id,
    #         oi.product_id
    #     FROM order_items oi
    #     JOIN orders o ON o.id = oi.order_id
    # """, connection)

    if df.empty:
        print("No order data found for market basket.")
        return

    basket = (
        df.groupby(['order_id', 'product_id'])
          .size()
          .unstack(fill_value=0)
    )

    basket = basket.map(lambda x: 1 if x > 0 else 0)

    frequent_itemsets = fpgrowth(
        basket,
        min_support=0.01,
        use_colnames=True
    )

    if frequent_itemsets.empty:
        print("No frequent itemsets found.")
        return

    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=1.1
    )

    if rules.empty:
        print("No association rules generated.")
        return

    with open(BASKET_PATH, "wb") as f:
        pickle.dump(rules, f)

    print(f"Market basket rules saved to {BASKET_PATH}")
