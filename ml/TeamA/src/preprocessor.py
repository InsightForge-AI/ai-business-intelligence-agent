import pandas as pd
import numpy as np


def preprocess(filepath):

    df = pd.read_csv(filepath)

    # removing duplicate rows
    df = df.drop_duplicates()

    # converting text columns values to title case and removing extra spaces
    for col in ['product', 'region', 'salesperson', 'category']:
        df[col] = df[col].astype(str).str.strip().str.title()

    # after applying str.title(), NaN becomes the string "Nan"
    # converting it back to actual NaN so we can fill it properly
    df[['region', 'salesperson']] = df[['region', 'salesperson']].replace('Nan', np.nan)

    # filling missing categorical values with the most frequent value
    for col in ['region', 'salesperson']:
        df[col] = df[col].fillna(df[col].mode()[0])

    # cleaning unit_price first before filling nulls
    # some entries have text like "55000 INR" so we remove non-numeric characters
    df['unit_price'] = df['unit_price'].astype(str).str.replace(r'[^0-9.]', '', regex=True)
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())

    # converting quantity and discount to numeric
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['discount'] = pd.to_numeric(df['discount'], errors='coerce')
    df['discount'] = df['discount'].fillna(df['discount'].median())

    # some discount values were entered as 15 instead of 0.15
    # dividing by 100 to bring them to the correct decimal format
    df.loc[df['discount'] > 1, 'discount'] /= 100

    # removing rows where quantity is zero or negative as they are not valid orders
    df = df[df['quantity'] > 0]

    # converting total_sales to numeric and removing negative or zero values
    # negative sales have no business meaning so we drop them
    df['total_sales'] = pd.to_numeric(df['total_sales'], errors='coerce')
    df = df[df['total_sales'] > 0]
    df['total_sales'] = df['total_sales'].fillna(df['total_sales'].median())

    # converting the date column to datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    # keeping only the columns needed for analysis
    df = df[['date', 'product', 'region', 'total_sales']]

    # dropping duplicates again after column selection
    # two rows might look different with all columns but become identical once we trim down to 4
    df = df.drop_duplicates()

    df = df.reset_index(drop=True)


    return df

if __name__ == "__main__":
    df = preprocess("ml/TeamA/data/sales_data.csv")
    print(df.head())