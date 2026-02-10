import pickle
from recommendations.services.redis_client import get_redis

BASKET_PATH = "recommendations/data/basket_rules.pkl"
GLOBAL_FALLBACK_KEY = "global:top_products"

def store_bought_together_in_redis():
    r = get_redis()
    global_products = r.get(GLOBAL_FALLBACK_KEY)
    global_products = global_products.split(",") if global_products else []

    with open(BASKET_PATH, "rb") as f:
        rules = pickle.load(f)

    if rules.empty:
        print("No basket rules to store.")
        return

    # Clear old keys
    for key in r.scan_iter("product:*:bought_together"):
        r.delete(key)

    seen_products = set()
    
    for _, row in rules.iterrows():
        antecedents = row["antecedents"]
        consequents = row["consequents"]

        # Use lift as score (or confidence)
        score = float(row["lift"])

        for a in antecedents:
            seen_products.add(a)
            for c in consequents:
                r.zadd(
                    f"product:{a}:bought_together",
                    {str(c): score}
                )

    for product_id in global_products:
        key = f"product:{product_id}:bought_together"
        if not r.exists(key):
            for fallback_product in global_products[:10]:
                if fallback_product != product_id:
                    r.zadd(key, {fallback_product: 0.1})