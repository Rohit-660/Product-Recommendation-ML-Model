import pickle
from recommendations.services.redis_client import get_redis

ALS_MODEL_PATH = "recommendations/data/als_model.pkl"

def generate_top_buys_from_model():
    r = get_redis()

    with open(ALS_MODEL_PATH, "rb") as f:
        model, users, products, matrix = pickle.load(f)

    for user_idx, user_id in enumerate(users):
        user_items = matrix[user_idx]

        # 🔑 IMPORTANT: unpack explicitly
        item_ids, scores = model.recommend(
            user_idx,
            user_items,
            N=10
        )

        # item_ids may be float32 → cast to int
        product_ids = [str(products[int(i)]) for i in item_ids]

        r.set(f"user:{user_id}:top_buys", ",".join(product_ids))