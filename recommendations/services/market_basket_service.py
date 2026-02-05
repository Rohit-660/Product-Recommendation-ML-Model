import pickle
from recommendations.services.redis_client import get_redis

BASKET_PATH = "recommendations/data/basket_rules.pkl"

def store_bought_together_in_redis():
    r = get_redis()

    with open(BASKET_PATH, "rb") as f:
        rules = pickle.load(f)

    if rules.empty:
        print("No basket rules to store.")
        return

    # Clear old keys
    for key in r.scan_iter("product:*:bought_together"):
        r.delete(key)

    for _, row in rules.iterrows():
        antecedents = row["antecedents"]
        consequents = row["consequents"]

        # Use lift as score (or confidence)
        score = float(row["lift"])

        for a in antecedents:
            for c in consequents:
                r.zadd(
                    f"product:{a}:bought_together",
                    {str(c): score}
                )