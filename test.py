import sqlite3
import random
from faker import Faker
from datetime import datetime

fake = Faker()

# اتصال به دیتابیس
conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

# پاک کردن رکوردهای قبلی (اختیاری)
for table in ["Product_category", "Product_subcategory", "Product_product",
              "Product_colors", "Product_size", "Account_user"]:
    cur.execute(f"DELETE FROM {table};")

# --- Product_category ---
categories = [(fake.word(), f"https://picsum.photos/50/50?random={i}") for i in range(1, 11)]
cur.executemany("INSERT INTO Product_category (name, icon) VALUES (?, ?)", categories)

# --- Product_subcategory ---
subcategories = [(fake.word(), f"https://picsum.photos/60/60?random={i}", random.randint(1, 10)) for i in range(1, 11)]
cur.executemany("INSERT INTO Product_subcategory (name, icon, category_id) VALUES (?, ?, ?)", subcategories)

# --- Product_colors ---
colors = [(fake.color_name(),) for _ in range(10)]
cur.executemany("INSERT INTO Product_colors (color_name) VALUES (?)", colors)

# --- Product_size ---
sizes = [(random.choice(["XS", "S", "M", "L", "XL", "XXL"]),) for _ in range(10)]
cur.executemany("INSERT INTO Product_size (size) VALUES (?)", sizes)

# --- Product_product ---
products = [(fake.word(), fake.text(max_nb_chars=100), random.randint(1, 200),
             random.randint(1, 10)) for _ in range(10)]
cur.executemany("INSERT INTO Product_product (name, descriptions, count, sub_category_id) VALUES (?, ?, ?, ?)", products)

# --- Account_user ---
users = []
for _ in range(10):
    users.append((
        fake.password(),
        None,  # last_login
        random.choice([0, 1]),  # is_superuser
        fake.user_name(),
        fake.first_name(),
        fake.last_name(),
        fake.email(),
        random.choice([0, 1]),  # is_staff
        1,  # is_active
        datetime.now().isoformat(" ")  # date_joined
    ))

cur.executemany("""
INSERT INTO Account_user 
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", users)

conn.commit()
conn.close()

print("✅ دیتای فیک با موفقیت اضافه شد!")
