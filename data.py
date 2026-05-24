import pandas as pd
import re

# ── 1. Load Data ──────────────────────────────────────────────────────────────
# Update this path to where your CSV file is saved on your computer
df = pd.read_csv('customer_shopping_behavior.csv')

# ── 2. Explore Data ───────────────────────────────────────────────────────────
print(df.head())
print(df.info())
print(df.describe(include='all'))
print(df.isnull().sum())

# ── 3. Handle Missing Values ──────────────────────────────────────────────────
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(
    lambda x: x.fillna(x.mean())
)
print(df.isnull().sum())

# ── 4. Rename Columns to snake_case ──────────────────────────────────────────
def to_snake_case(name):
    name = re.sub(r'[^a-zA-Z0-9_ ]', ' ', name)
    name = re.sub(r'([a-z])(id|amount|purchased|rating|status|type|applied|used|purchases|method|frequency|usd)\b', r'\1_\2', name)
    name = name.lower()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'_{2,}', '_', name)
    name = name.strip('_')
    return name

df.columns = [to_snake_case(col) for col in df.columns]
print(df.columns)

# ── 5. Feature Engineering ────────────────────────────────────────────────────
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)
print(df[['age', 'age_group']].head(10))

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['purchase_frequency_days', 'frequency_of_purchases']].head(10))

# ── 6. Drop Redundant Column ──────────────────────────────────────────────────
print(df[['discount_applied', 'promo_code_used']].head(10))
print((df['discount_applied'] == df['promo_code_used']).all())
df = df.drop('promo_code_used', axis=1)
print(df.columns)

# ── 7. Load into PostgreSQL ───────────────────────────────────────────────────
from sqlalchemy import create_engine

username = "postgres"
password = "Raiyaa_21"
host = "localhost"
port = "5432"
database = "customer_behaviour"

engine = create_engine(f"postgresql+psycopg2://postgres:Raiyaa_21@localhost:5432/customer_behaviour")

table_name = "customer"
df.to_sql(table_name, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")