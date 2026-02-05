# Recommendation System

This project implements a product recommendation system using Django, Python, PostgreSQL, Redis, and Pickle.

The system trains models offline and serves recommendations using Redis for fast responses.

## What this system does

The system provides two types of recommendations.

Top Buys
- Personalized recommendations for logged-in users
- Global popular products for guest users

Bought Together
- Same recommendations for all users
- Products frequently purchased together

## Algorithms used

ALS (Alternating Least Squares)
- Used for personalized recommendations
- Works with implicit feedback such as purchases

Market Basket Optimization (FP-Growth)
- Used for bought together recommendations
- Finds products that appear together in orders

## Technology stack

- Django
- Python
- PostgreSQL
- Redis
- Pickle

## How the system works

- Orders are stored in PostgreSQL
- User-product interactions are updated incrementally
- Models are trained offline
- Trained models are saved using Pickle
- Recommendation results are stored in Redis
- APIs read data only from Redis

## Project structure

recommendations
- api
- services
- management
- data

The data folder is created automatically by batch jobs.

## How to run locally

Start Redis

redis-server

Run batch jobs

    python manage.py update_interactions
    python manage.py train_als_model
    python manage.py generate_top_buys
    python manage.py generate_global_top_buys
    python manage.py train_market_basket
    python manage.py generate_bought_together

Start Django

python manage.py runserver

## API endpoints

Top Buys
> <ins>/api/recommendations/top-buys/?user_id=123</ins>

Bought Together
> <ins>/api/recommendations/bought-together/{product_id}/</ins>

## Summary

This system trains recommendation models offline, stores results in Redis, and serves fast APIs without recomputation.
