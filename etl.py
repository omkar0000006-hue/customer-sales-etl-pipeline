import pandas as pd
import sqlite3
import logging
import os
from datetime import datetime

os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Pipeline Started")

print(f"Pipeline executed at {datetime.now()}")

logging.info(f"Pipeline executed at {datetime.now()}")


try:

    df = pd.read_csv("data/sales_data.csv")

    print("Raw Data")
    print(df)

   

except Exception as e:
    logging.error(f"Pipeline Failed: {e}")
    print(f"Error: {e}")


if df.isnull().sum().sum() > 0:
    print("Missing values found")
    logging.warning("Missing values found in dataset")


df["total_amount"] = df["quantity"] * df["price"]

df = df.drop_duplicates()

print("\nTransformed Data")
print(df)


conn = sqlite3.connect("output/sales.db")

df.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False
)

print("\nData Loaded Successfully")
logging.info("Data Loaded Successfully")


report = pd.read_sql_query("""
SELECT
    customer,
    SUM(total_amount) AS total_spent
FROM sales
GROUP BY customer
ORDER BY total_spent DESC
""", conn)

print("\nCustomer Spending Report")
print(report)

report.to_csv(
    "output/customer_report.csv",
    index=False
)


product_report = pd.read_sql_query("""
SELECT
    product,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY product
ORDER BY total_quantity DESC
""", conn)

print("\nProduct Performance Report")
print(product_report)

product_report.to_csv(
    "output/product_report.csv",
    index=False
)


conn.close()

logging.info("Pipeline Completed Successfully")