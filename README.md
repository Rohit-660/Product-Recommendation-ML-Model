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

Run following queries into your database

    CREATE TABLE batch_metadata (
      job_name TEXT PRIMARY KEY,
      last_processed_at TIMESTAMP
    );
    
    INSERT INTO batch_metadata
    VALUES ('order_delta', '1970-01-01');

    CREATE TABLE user_product_interactions (
      user_id INT,
      product_id INT,
      interaction_score FLOAT,
      last_updated_at TIMESTAMP,
      PRIMARY KEY (user_id, product_id)
    );

Clone the project using folllowing command
    
    git clone https://github.com/Rohit-660/Product-Recommendation-ML-Model

Update databse credentials in reco/settings.py

Create Python Virtual Enviornment using folllowing command

    python -m venv ml-env

Activate it Enviornment using folllowing command

    ..\ml-env\Scripts\Activate.ps1

Install all the required packages

    pip install -r requirements.txt
    
Start Redis

Start Django

    python manage.py runserver

Run batch jobs

    python manage.py update_interactions
    python manage.py train_als_model
    python manage.py generate_top_buys
    python manage.py train_market_basket
    python manage.py store_market_basket

## API endpoints

Top Buys
> <ins>/api/recommendations/top-buys/?user_id=123</ins>

Bought Together
> <ins>/api/recommendations/bought-together/{product_id}/</ins>

## Summary

This system trains recommendation models offline, stores results in Redis, and serves fast APIs without recomputation.
