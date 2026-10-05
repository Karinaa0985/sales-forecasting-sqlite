import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "Superstore.xls")
DB_PATH = os.path.join(BASE_DIR, "superstore.db")

# Load dataset
if os.path.exists(DATA_PATH.replace(".xls", ".xlsx")):
    df = pd.read_excel(DATA_PATH.replace(".xls", ".xlsx"))
elif os.path.exists(DATA_PATH.replace(".xls", ".csv")):
    df = pd.read_csv(DATA_PATH.replace(".xls", ".csv"), encoding="latin1")
else:
    df = pd.read_excel(DATA_PATH)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")

# Print detected column names to verify
print("\nDetected Columns in Dataset:", df.columns.tolist())

# Map common column variations
col_mapping = {}
for col in df.columns:
    if col in ['order_date', 'orderdate', 'date']:
        col_mapping[col] = 'order_date'
    elif col in ['category', 'product_category', 'dept']:
        col_mapping[col] = 'category'
    elif col in ['region', 'territory']:
        col_mapping[col] = 'region'
    elif col in ['sales', 'total_sales', 'sales_amount']:
        col_mapping[col] = 'sales'
    elif col in ['profit', 'total_profit']:
        col_mapping[col] = 'profit'
    elif col in ['order_id', 'orderid', 'id']:
        col_mapping[col] = 'order_id'

df = df.rename(columns=col_mapping)

# Ensure order_date is formatted cleanly
df['order_date'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d')

# Save to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

df.to_sql("sales_raw", conn, if_exists="replace", index=False)

cursor.execute("DROP TABLE IF EXISTS monthly_sales_summary;")

cursor.execute("""
    CREATE TABLE monthly_sales_summary AS
    SELECT 
        strftime('%Y-%m', order_date) AS sales_month,
        category,
        region,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        COUNT(order_id) AS total_orders
    FROM sales_raw
    GROUP BY sales_month, category, region;
""")

conn.commit()
conn.close()

print("\nDatabase superstore.db built successfully!")