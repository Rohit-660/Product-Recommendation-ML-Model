import pickle
from recommendations.services.redis_client import get_redis

ALS_MODEL_PATH = "recommendations/data/als_model.pkl"
GLOBAL_FALLBACK_KEY = "global:top_products"

def generate_top_buys_from_model():
    r = get_redis()

    global_products = r.get(GLOBAL_FALLBACK_KEY)
    global_products = global_products.split(",") if global_products else []

    with open(ALS_MODEL_PATH, "rb") as f:
        model, users, products, matrix = pickle.load(f)

    for user_idx, user_id in enumerate(users):
        user_items = matrix[user_idx]

        item_ids, scores = model.recommend(
            user_idx,
            user_items,
            N=10
        )

        if len(item_ids) > 0:
            product_ids = [str(products[int(i)]) for i in item_ids]
        else:
            product_ids = global_products[:10]


        r.set(f"user:{user_id}:top_buys", ",".join(product_ids))