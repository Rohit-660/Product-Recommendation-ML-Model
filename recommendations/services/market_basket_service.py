import pandas as pd
import pickle
from mlxtend.frequent_patterns import fpgrowth, association_rules
from django.db import connection

BASKET_PATH = "recommendations/data/basket_rules.pkl"

def train_and_save_market_basket():
    # -------------------------------
    # STEP 1: Fetch order data
    # -------------------------------
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT oi.order_id, oi.product_id
            FROM order_items oi
            JOIN orders o ON o.id = oi.order_id
            WHERE o.created_at > now() - interval '180 days'
        """)
        rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=["order_id", "product_id"])

    if df.empty:
        print("No order data found. Skipping market basket.")
        return

    # -------------------------------
    # STEP 2: Remove single-item orders
    # -------------------------------
    order_sizes = df.groupby("order_id").size()
    valid_orders = order_sizes[order_sizes > 1].index
    df = df[df["order_id"].isin(valid_orders)]

    if df.empty:
        print("No multi-item orders found. Skipping market basket.")
        return

    # -------------------------------
    # STEP 3: Build basket matrix
    # -------------------------------
    basket = (
        df.groupby(["order_id", "product_id"])
          .size()
          .unstack(fill_value=0)
    )

    # Replace deprecated applymap
    basket = basket.gt(0).astype(int)

    # -------------------------------
    # STEP 4: Run FP-Growth (LOWER SUPPORT)
    # -------------------------------
    freq = fpgrowth(
        basket,
        min_support=0.001,   # 🔥 lowered to 0.1%
        use_colnames=True
    )

    if freq.empty:
        print("No frequent itemsets found. Skipping rules generation.")
        return

    # -------------------------------
    # STEP 5: Generate rules
    # -------------------------------
    rules = association_rules(
        freq,
        metric="lift",
        min_threshold=1.1
    )

    if rules.empty:
        print("No association rules found. Skipping save.")
        return

    # -------------------------------
    # STEP 6: Save rules
    # -------------------------------
    with open(BASKET_PATH, "wb") as f:
        pickle.dump(rules, f)

    print(f"Market basket rules saved: {len(rules)} rules")