
# ============================================================
# CUSTOMER SHOPPING BEHAVIOR ANALYSIS
# DATA CLEANING & FEATURE ENGINEERING
# ============================================================


# STEP 1: IMPORT LIBRARIES

import pandas as pd


# STEP 2: LOAD DATASET (ONLY ONCE)

df = pd.read_csv('customer_shopping_behavior.csv')

print("\n========== ORIGINAL DATASET ==========")

print(df.head())
print("\nDataset Shape:", df.shape)
print("\nDataset Information:")
df.info()


# STEP 3: STANDARDIZE COLUMN NAMES

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_', regex=False)
)

# Rename purchase amount column

df = df.rename(columns={
    'purchase_amount_(usd)': 'purchase_amount'
})

print("\n========== STANDARDIZED COLUMNS ==========")

print(df.columns.tolist())


# STEP 4: DATA CLEANING

# 4.1 Check missing values before cleaning

print("\n========== MISSING VALUES BEFORE CLEANING ==========")

print(df.isnull().sum())


# 4.2 Replace missing Review Ratings
# Using category-wise median

df['review_rating'] = df.groupby('category')['review_rating'].transform(
    lambda x: x.fillna(x.median())
)


# 4.3 Remove duplicate records

duplicates = df.duplicated().sum()

print("\nDuplicate Records:", duplicates)

df = df.drop_duplicates()


# 4.4 Check and remove redundant columns

print("\n========== DISCOUNT COLUMN COMPARISON ==========")

print(df[['discount_applied', 'promo_code_used']].head(10))

if df['discount_applied'].equals(df['promo_code_used']):

    df = df.drop(columns=['promo_code_used'])

    print("\nRedundant column 'promo_code_used' removed successfully!")

else:

    print("\nBoth columns contain different values. No column removed.")


# 4.5 Check missing values after cleaning

print("\n========== MISSING VALUES AFTER CLEANING ==========")

print(df.isnull().sum())


# STEP 5: FEATURE ENGINEERING

# 5.1 Create Age Groups using Quartiles

labels = ['Young_Adult', 'Adult', 'Middle_Aged', 'Senior']

df['age_group'] = pd.qcut(
    df['age'],
    q=4,
    labels=labels
)

print("\n========== AGE GROUP DISTRIBUTION ==========")

print(df['age_group'].value_counts())


# 5.2 Convert Purchase Frequency into Days

frequency_mapping = {
    'fortnightly': 14,
    'weekly': 7,
    'monthly': 30,
    'quarterly': 90,
    'bi-weekly': 14,
    'annually': 365,
    'every 3 months': 90
}

df['purchase_frequency_days'] = (
    df['frequency_of_purchases']
    .str.strip()
    .str.lower()
    .map(frequency_mapping)
)


# Check unmapped purchase frequencies

print("\n========== FREQUENCY MAPPING CHECK ==========")

print("Unmapped Values:",
      df['purchase_frequency_days'].isnull().sum())

unmapped = df.loc[
    df['purchase_frequency_days'].isnull(),
    'frequency_of_purchases'
].unique()

if len(unmapped) > 0:
    raise ValueError(f"Unmapped purchase frequencies: {unmapped}")


# STEP 6: FINAL DATA VALIDATION

print("\n========== FINAL DATASET ==========")

print(df.head(10))

print("\nFinal Dataset Shape:", df.shape)

print("\nFinal Column Names:")

print(df.columns.tolist())

print("\nFinal Missing Values:")

print(df.isnull().sum())


# STEP 7: EXPORT CLEANED DATASET

df.to_csv(
    'customer_shopping_behavior_cleaned.csv',
    index=False
)

print("\n========== PROJECT COMPLETED ==========")

print("Cleaned dataset exported successfully!")

print("Final Records:", len(df))

print("Final Columns:", len(df.columns))

#Add this terminal :python -m pip install sqlalchemy psycopg2-binary


from sqlalchemy import create_engine

# Step 1: Connect to PostgreSQL

username = "add username here"
password = "add password here"
host = "add host here"
port = "add port here"
database = "customer_behavior"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

# Step 2: Export DataFrame to PostgreSQL

table_name = "customer"

df.to_sql(
    name=table_name,
    con=engine,
    if_exists="replace",
    index=False
)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")



