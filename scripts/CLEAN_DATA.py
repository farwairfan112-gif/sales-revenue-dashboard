import pandas as pd

df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')

print("Shape:", df.shape)
print("\nMissing values:\n", df.isnull().sum())

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date']  = pd.to_datetime(df['Ship Date'])

df['Order Year']      = df['Order Date'].dt.year
df['Order Month']     = df['Order Date'].dt.month
df['Order Month Name']= df['Order Date'].dt.strftime('%b')
df['Days to Ship']    = (df['Ship Date'] - df['Order Date']).dt.days

df['Postal Code'] = df['Postal Code'].astype(str)

before = len(df)
df.drop_duplicates(inplace=True)
print(f"\nDuplicates removed: {before - len(df)}")

str_cols = df.select_dtypes(include='object').columns
df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

print("\n── Key Metrics ──────────────────────────────")
print(f"Total Revenue:  ${df['Sales'].sum():,.0f}")
print(f"Total Profit:   ${df['Profit'].sum():,.0f}")
print(f"Profit Margin:  {(df['Profit'].sum()/df['Sales'].sum()*100):.1f}%")
print(f"Total Orders:   {df['Order ID'].nunique():,}")
print(f"Date Range:     {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")

print(f"\nSales by Region:")
print(df.groupby('Region')['Sales'].sum().sort_values(ascending=False))

print(f"\nProfit by Category:")
print(df.groupby('Category')['Profit'].sum().sort_values(ascending=False))

print(f"\nProfit by Sub-Category (bottom 5):")
print(df.groupby('Sub-Category')['Profit'].sum().sort_values().head(5))

df.to_csv('superstore_clean.csv', index=False)
print("\n✓ Saved: superstore_clean.csv")