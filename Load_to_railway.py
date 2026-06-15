from pathlib import Path
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

# ==========================
# Railway Connection
# ==========================
load_dotenv()
conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = conn.cursor()

print("Connected to Railway MySQL")


# ==========================
# Locate Exports Folder
# ==========================

possible_paths = [
    Path("Exports"),
    Path("/opt/project/Exports"),
    Path(__file__).parent / "Exports"
]

BASE_PATH = None

for path in possible_paths:
    if path.exists():
        BASE_PATH = path
        break

if BASE_PATH is None:
    raise FileNotFoundError(
        "Exports folder not found"
    )

print(f"Using exports folder: {BASE_PATH.resolve()}")


# ==========================
# Create Tables
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_customer(
    customer_key BIGINT,
    customer_id BIGINT,
    customer_name VARCHAR(100),
    customer_city VARCHAR(100),
    customer_state VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_product(
    product_key BIGINT,
    product_id BIGINT,
    product_name VARCHAR(100),
    category VARCHAR(100),
    price DOUBLE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_orders(
    order_id BIGINT,
    customer_id BIGINT,
    product_id BIGINT,
    quantity BIGINT,
    amount DOUBLE
)
""")

conn.commit()

print("Tables verified")


# ==========================
# Validate Files
# ==========================

required_files = [
    "dim_customer.csv",
    "dim_product.csv",
    "fact_orders.csv"
]

for file in required_files:

    file_path = BASE_PATH / file

    if not file_path.exists():

        raise FileNotFoundError(
            f"{file} not found at {file_path}"
        )

print("All CSV files found")


# ==========================
# Read CSV Files
# ==========================

customer_df = pd.read_csv(
    BASE_PATH / "dim_customer.csv"
)

product_df = pd.read_csv(
    BASE_PATH / "dim_product.csv"
)

orders_df = pd.read_csv(
    BASE_PATH / "fact_orders.csv"
)

print("CSV files loaded")


# ==========================
# Data Quality Checks
# ==========================

if customer_df.empty:
    raise ValueError(
        "dim_customer.csv is empty"
    )

if product_df.empty:
    raise ValueError(
        "dim_product.csv is empty"
    )

if orders_df.empty:
    raise ValueError(
        "fact_orders.csv is empty"
    )

print(f"Customer rows: {len(customer_df)}")
print(f"Product rows: {len(product_df)}")
print(f"Order rows: {len(orders_df)}")


# ==========================
# Make Pipeline Idempotent
# ==========================

cursor.execute("TRUNCATE TABLE fact_orders")
cursor.execute("TRUNCATE TABLE dim_product")
cursor.execute("TRUNCATE TABLE dim_customer")

conn.commit()

print("Existing data cleared")


# ==========================
# Insert Customers
# ==========================

customer_records = list(
    customer_df.itertuples(
        index=False,
        name=None
    )
)

cursor.executemany(
    """
    INSERT INTO dim_customer
    VALUES (%s,%s,%s,%s,%s)
    """,
    customer_records
)

print(
    f"{len(customer_records)} customers loaded"
)


# ==========================
# Insert Products
# ==========================

product_records = list(
    product_df.itertuples(
        index=False,
        name=None
    )
)

cursor.executemany(
    """
    INSERT INTO dim_product
    VALUES (%s,%s,%s,%s,%s)
    """,
    product_records
)

print(
    f"{len(product_records)} products loaded"
)


# ==========================
# Insert Orders
# ==========================

order_records = list(
    orders_df.itertuples(
        index=False,
        name=None
    )
)

cursor.executemany(
    """
    INSERT INTO fact_orders
    VALUES (%s,%s,%s,%s,%s)
    """,
    order_records
)

print(
    f"{len(order_records)} orders loaded"
)

conn.commit()

print("Data loaded successfully")

cursor.close()
conn.close()

print("Connection closed")