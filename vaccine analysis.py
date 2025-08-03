import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load datasets from xlsx and convert to csv
file_paths = {
    "coverage_data": "C:/Users/Administrator/OneDrive/Documents/DS projects/coverage-data.xlsx",
    "incidence_rate": "C:/Users/Administrator/OneDrive/Documents/DS projects/incidence-rate-data.xlsx",
    "reported_cases": "C:/Users/Administrator/OneDrive/Documents/DS projects/reported-cases-data.xlsx",
    "vaccine_introduction": "C:/Users/Administrator/OneDrive/Documents/DS projects/vaccine-introduction-data.xlsx",
    "vaccine_schedule": "C:/Users/Administrator/OneDrive/Documents/DS projects/vaccine_schedule.xlsx"
}

datasets = {}

# Read xlsx files and convert to csv
for name, path in file_paths.items():
    if os.path.exists(path):  # Check if file exists
        try:
            df = pd.read_excel(path, engine="openpyxl")
            csv_path = f"{name}.csv"
            df.to_csv(csv_path, index=False)
            datasets[name] = df
            print(f"Successfully loaded and converted {name} dataset to {csv_path}")
        except Exception as e:
            print(f"Error reading {name}: {e}")
    else:
        print(f"File not found: {path}")

# Function to clean data
def clean_data(df, name):
    print(f"\nCleaning {name} dataset...")

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df.ffill(inplace=True)  # Forward fill missing values

    # Convert column names to lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Ensure 'year' column is in correct format
    if 'year' in df.columns:
        df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.year

    print(f"{name} dataset cleaned successfully!\n")
    return df

# Apply cleaning function to all datasets
for name in datasets.keys():
    datasets[name] = clean_data(datasets[name], name)

# Save cleaned datasets
for name, df in datasets.items():
    df.to_csv(f"cleaned_{name}.csv", index=False)

print("Data Cleaning Completed Successfully!\n")

# Exploratory Data Analysis (EDA)
print("Starting EDA...\n")

def perform_eda(df, name):
    print(f"EDA for {name} dataset:\n")

    # Display basic info
    print(df.info())

    # Summary statistics
    print("\nSummary Statistics:\n", df.describe())

    # Check missing values
    print("\nMissing Values:\n", df.isnull().sum())

    # Distribution of numerical columns
    df.select_dtypes(include=['number']).hist(figsize=(10, 6))
    plt.suptitle(f"Histograms for {name} Dataset")
    plt.show()

    # Correlation matrix for numerical data
    numeric_df = df.select_dtypes(include=['number'])  # Select numeric columns
    if numeric_df.shape[1] > 1:
        plt.figure(figsize=(8, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
        plt.title(f"Correlation Matrix - {name}")
        plt.show()

    print("\nEDA Completed for", name, "\n")

# Perform EDA on all datasets
for name, df in datasets.items():
    perform_eda(df, name)

print("EDA Process Completed Successfully!")