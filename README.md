Recommendation System (Top Buys & Bought Together)

This project implements a product recommendation system using Django, Python, PostgreSQL, Redis, and Pickle.

The system is designed to work efficiently on large datasets by avoiding repeated data crawling and running machine learning offline.

What this system does

The system provides two types of recommendations:

1. Top Buys

  For logged-in users: personalized recommendations using their purchase history

  For guest users: global popular products

2. Bought Together

  Same for all users
  
  Products frequently purchased together
  
  Ordered by strength (lift)

Algorithms Used
  ALS (Alternating Least Squares)

    Used for personalized Top Buys
    
    Works with implicit feedback (purchases, not ratings)
    
    Learns hidden patterns between users and products

  Market Basket Optimization (FP-Growth)

    Used for Bought Together

    Finds products that appear together in orders
    
    Generates association rules based on support and lift

Tech Stack

  Backend: Django
  
  Database: PostgreSQL
  
  Cache: Redis
  
  ML: Python
  
  Model storage: Pickle
  
  Algorithms: ALS, FP-Growth

High Level Flow

  Read order data from PostgreSQL
  
  Update user-product interactions incrementally
  
  Train ML models offline
  
  Save trained models as Pickle files
  
  Generate recommendations and store them in Redis
  
  APIs read data only from Redis
  
  No ML runs during API requests.

Required helper tables:

batch_metadata
- job_name
- last_processed_at

user_product_interactions
- user_id
- product_id
- interaction_score
- last_updated_at

These tables help avoid reprocessing all data.

Redis Key Structure

  user:{id}:top_buys → personalized recommendations
  
  global:top_buys → guest user recommendations
  
  product:{id}:bought_together → bought together products (sorted set)

How to Run Locally
  1. Start Redis
    redis-server
  
  2. Run batch jobs (in order)
    python manage.py update_interactions
    python manage.py train_als_model
    python manage.py generate_top_buys
    python manage.py generate_global_top_buys
    python manage.py train_market_basket
    python manage.py generate_bought_together
  
  3. Start Django server
    python manage.py runserver

API Endpoints

Top Buys
  GET /api/recommendations/top-buys/?user_id=123

Bought Together
  GET /api/recommendations/bought-together/{product_id}/
