import json
import random
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

fake = Faker()

# Directory to save files
output_dir = Path("/mnt/data/json_samples")
output_dir.mkdir(parents=True, exist_ok=True)

# Generate 1000 users
users = []
for i in range(1, 1001):
    users.append({
        "user_id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "signup_date": fake.date_between(start_date='-2y', end_date='today').isoformat()
    })

# Generate 1000 orders with nested structure
orders = []
for i in range(1, 1001):
    num_items = random.randint(1, 4)
    items = [{
        "product_id": random.randint(1, 500),
        "quantity": random.randint(1, 5),
        "price": round(random.uniform(5, 500), 2)
    } for _ in range(num_items)]

    orders.append({
        "order_id": i,
        "order_date": fake.date_between(start_date='-1y', end_date='today').isoformat(),
        "customer": {
            "customer_id": random.randint(1, 1000),
            "name": fake.name(),
            "email": fake.email()
        },
        "items": items,
        "status": random.choice(["shipped", "pending", "delivered", "cancelled"])
    })

# Generate 1000 products with mixed structure
products = []
for i in range(1, 1001):
    products.append({
        "product_id": i,
        "name": fake.word().capitalize(),
        "categories": fake.words(nb=random.randint(1, 3),
                                 ext_word_list=["Electronics", "Audio", "Computers", "Books", "Clothing", "Toys"]),
        "price": round(random.uniform(10, 1000), 2),
        "available": fake.boolean(),
        "metadata": {
            "brand": fake.company(),
            "warranty_years": random.randint(1, 3)
        }
    })

# Write files
users_path = output_dir / "users.json"
orders_path = output_dir / "orders.json"
products_path = output_dir / "products.json"

with users_path.open("w") as f:
    json.dump(users, f, indent=2)

with orders_path.open("w") as f:
    json.dump(orders, f, indent=2)

with products_path.open("w") as f:
    json.dump(products, f, indent=2)

users_path.name, orders_path.name, products_path.name
