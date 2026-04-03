import pandas as pd

def analyze(df):
    """
    Analyzes sales data to calculate totals, top products, and trends.
    """
    # adding up all the sales to get the overall total
    total_sales = float(round(df['total_sales'].sum(), 2))

    # grouping by product and finding which one made the most money overall
    top_product = df.groupby('product')['total_sales'].sum().idxmax()

    # sorting records by date so we can compare early sales vs recent sales
    df = df.sort_values('date').reset_index(drop=True)
    mid = len(df) // 2
    first_half = df['total_sales'][:mid].mean()
    second_half = df['total_sales'][mid:].mean()

    # trend calculation logic
    if second_half > first_half * 1.05:
        trend = 'increasing'
    elif second_half < first_half * 0.95:
        trend = 'decreasing'
    else:
        trend = 'stable'

    return {
        'total_sales': total_sales,
        'top_product': top_product,
        'trend': trend
    }

if __name__ == "__main__":
    import os
    import sys
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ensure preprocessor can be imported
    if current_dir not in sys.path:
        sys.path.append(current_dir)
        
    from preprocessor import preprocess

    # Construct the path to the CSV file
    data_path = os.path.join(current_dir, '..', 'data', 'sales_data.csv')

    try:
        df = preprocess(data_path)
        result = analyze(df)
        
        print("Analysis Results:")
        for key, value in result.items():
            clean_key = key.replace('_', ' ').title()
            
            # If the key is total sales, format it as currency
            if key == 'total_sales':
                print(f"{clean_key}: ₹{value:,.2f}")  # Adds ₹ and commas (e.g., ₹63,954,961.36)
            else:
                print(f"{clean_key}: {value}")
            
    except FileNotFoundError:
        print(f"Error: Could not find the file at {data_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")