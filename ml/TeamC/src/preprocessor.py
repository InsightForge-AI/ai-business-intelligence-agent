import pandas as pd

def preprocess_data(sales_data):

    # Load dataset
    df = pd.read_csv("ml/TeamC/Data/Raw/sales_data.csv")

    print("Original Columns:", df.columns)

    # Clean column names 
    df.columns = df.columns.str.strip().str.lower()

    print("Cleaned Columns:", df.columns)

    print("Original Shape:", df.shape)

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    if 'total' in df.columns:
        df['total'] = df['total'].fillna(0)

    # Convert data types
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    if 'quantity' in df.columns:
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

    if 'total' in df.columns:
        df['total'] = pd.to_numeric(df['total'], errors='coerce')

    # Drop null values
    df = df.dropna()

    # Save cleaned data
    output_path = "ml/TeamC/Data/Cleaned/cleaned_sales.csv"
    df.to_csv(output_path, index=False)

    print("Cleaned data saved to:", output_path)

    return df


# Run
if __name__ == "__main__":
    preprocess_data("ml/TeamC/Data/Raw/sales_data.csv")