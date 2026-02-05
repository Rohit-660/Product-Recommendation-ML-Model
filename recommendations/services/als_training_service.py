import pandas as pd
import pickle
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
from django.db import connection

ALS_MODEL_PATH = "recommendations/data/als_model.pkl"

def train_and_save_als_model():
    # df = pd.read_sql("""
    #     SELECT user_id, product_id, interaction_score
    #     FROM user_product_interactions
    # """, connection)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT user_id, product_id, interaction_score
            FROM user_product_interactions
        """)
        rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=["user_id", "product_id", "interaction_score"])

    users = df["user_id"].astype("category")
    products = df["product_id"].astype("category")

    matrix = coo_matrix(
        (df["interaction_score"],
         (users.cat.codes, products.cat.codes))
    ).tocsr()

    model = AlternatingLeastSquares(
        factors=64,
        iterations=15,
        regularization=0.1
    )

    model.fit(matrix)

    products = list(products.cat.categories)
    users = list(users.cat.categories)

    with open(ALS_MODEL_PATH, "wb") as f:
        pickle.dump(
            (model, users, products, matrix),
            f
        )
