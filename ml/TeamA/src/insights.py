import pandas as pd
import json

def get_final_report(df, analysis_results):
    """
    Combines raw analysis with a generated narrative for API output.
    """
    # Extract values from analysis_results
    raw_total_sales = analysis_results['total_sales']
    top_p = analysis_results['top_product']
    trend = analysis_results['trend']

    # Formatting total_sales with Rupee symbol and commas
    total_sales_formatted = f"₹{raw_total_sales:,.2f}"

    # 1. Top Product Percentage Calculation
    product_totals = df.groupby('product')['total_sales'].sum()
    top_product_revenue = product_totals.max()
    top_product_pct = (top_product_revenue / raw_total_sales) * 100

    # 2. Regional Contribution
    # Uses 'region' and 'total_sales' cleaned by preprocessor.py
    top_region = df.groupby('region')['total_sales'].sum().idxmax()
    
    # 3. Human-readable Trend mapping [cite: 1]
    trend_descriptions = {
        'increasing': "a positive growth trajectory",
        'decreasing': "a downward trend",
        'stable': "a steady and stable performance"
    }
    
    # Constructing the 'insights' string for the JSON response
    narrative = (
        f"{top_p} is the top product contributing {top_product_pct:.1f}% of sales. "
        f"The overall trend is {trend}, indicating {trend_descriptions.get(trend)}. "
        f"The {top_region} region is the leading market."
    )

    # Returning the dictionary structure required for your API response
    return {
        "total_sales": total_sales_formatted,
        "top_product": top_p,
        "trend": trend,
        "insights": narrative
    }

if __name__ == "__main__":
    from preprocessor import preprocess
    from analysis import analyze
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming standard project structure: /ml/TeamA/scripts/insights.py
    data_path = os.path.join(current_dir, '..', 'data', 'sales_data.csv')

    try:
        # Preprocessing the raw CSV data
        df = preprocess(data_path)
        # Core analysis
        results = analyze(df)
        
        # Generating the final report dictionary
        report = get_final_report(df, results)
        # Using ASCII value to properly use Rupee Symbol
        print(json.dumps(report, indent=4, ensure_ascii=False))
        
    except Exception as e:
        print(f"Test failed: {e}")