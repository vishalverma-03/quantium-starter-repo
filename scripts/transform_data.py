import pandas as pd
import glob
import os

# --- Locate data folder ---
current_dir = os.path.dirname(__file__)
data_folder = os.path.join(current_dir, "..", "data")
data_folder = os.path.abspath(data_folder)

# --- Get all CSVs in the data folder ---
csv_files = glob.glob(os.path.join(data_folder, "daily_sales_data_*.csv"))
print("Found CSV files:", csv_files)

# --- Read and combine all CSVs ---
dfs = [pd.read_csv(f) for f in csv_files]
data = pd.concat(dfs, ignore_index=True)

# --- Filter only 'pink morsel' products ---
data = data[data["product"] == "pink morsel"]

# --- Clean and convert price ---
data["price"] = data["price"].replace('[\$,]', '', regex=True).astype(float)

# --- Compute total sales ---
data["Sales"] = data["quantity"] * data["price"]

# --- Select only required columns ---
output_data = data[["Sales", "date", "region"]]

# --- Save to new CSV ---
output_path = os.path.join(data_folder, "cleaned_sales_data.csv")
output_data.to_csv(output_path, index=False)

print("✅ Cleaned data saved to:", output_path)
print("\n📊 Preview of cleaned data:")
print(output_data.head())
