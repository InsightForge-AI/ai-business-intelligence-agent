# ================================
# 📊 SALES DATA ANALYSIS PROJECT
# ================================

# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt

# ================================
# 📁 LOAD DATA
# ================================

# Load the cleaned dataset
df = pd.read_csv("C:/Users/GOLLAMUDI RAVINDRA/ai-business-intelligence-agent/ml/TeamC/Data/Cleaned/cleaned_sales.csv")

# Display first 5 rows
print("Preview of Data:\n", df.head())

# ================================
# 🔍 BASIC DATA UNDERSTANDING
# ================================

# Check data structure and types
print("\nData Info:\n")
print(df.info())

# Check missing values
print("\nMissing Values:\n", df.isnull().sum())

# Summary statistics
print("\nStatistical Summary:\n", df.describe())

# ================================
# 📈 BASIC ANALYSIS
# ================================

# Total sales
total_sales = df["total"].sum()
print("\nTotal Sales:", total_sales)

# Top selling products
print("\nTop Products:\n", df["product"].value_counts().head())

# Sales by category
print("\nSales by Category:\n", df.groupby("category")["total"].sum())

# Payment method distribution
print("\nPayment Methods:\n", df["payment_method"].value_counts())

# Order status distribution
print("\nOrder Status:\n", df["status"].value_counts())

# ================================
# 📊 VISUALIZATIONS
# ================================

# 1. Top Selling Products (Bar Chart)
top_products = df["product"].value_counts().head()

top_products.plot(kind="bar")
plt.title("Top Selling Products")
plt.xlabel("Product")
plt.ylabel("Count")
plt.show()

# 2. Sales by Category (Bar Chart)
category_sales = df.groupby("category")["total"].sum()

category_sales.plot(kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.show()

# 3. Sales Trend Over Time (Line Chart)

# Convert order_date to datetime
df["order_date"] = pd.to_datetime(df["order_date"])

# Group sales by date
sales_trend = df.groupby("order_date")["total"].sum()

# Plot trend
sales_trend.plot()
plt.title("Sales Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.show()

# ================================
# 🧠 BUSINESS INSIGHTS
# ================================

print("\n--- INSIGHTS ---")

print("1. Total Sales:", total_sales)

print("2. Top Product:\n", df["product"].value_counts().head(1))

print("3. Best Category:\n", df.groupby("category")["total"].sum().idxmax())

print("4. Most Used Payment Method:\n", df["payment_method"].value_counts().idxmax())

print("5. Order Status Summary:\n", df["status"].value_counts())