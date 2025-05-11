import requests
import pandas as pd

category_diff_file = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS4_-JR14aauzfKc2B5GGxXlDan9DGVx9RcBIGWVEZBNXbk-54_H-nv9Jqw2WAlATcglOgjuYy2Eye3/pub?gid=138894517&single=true&output=csv"
category_diff = pd.read_csv(category_diff_file)

# List of trade names
trade_names = category_diff["Category - Requests"].unique()

# API endpoint for creating trades
url = 'http://localhost:8000/api/trades/'

if __name__ == "__main__":
    # Create each trade
    for name in trade_names:
        response = requests.post(url, json={'name': name})
        if response.status_code == 201:
            print(f'Created trade: {name}')
        else:
            print(f'Failed to create trade: {name}, Status code: {response.status_code}') 