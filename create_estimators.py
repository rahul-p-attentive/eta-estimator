import os
import django
import sys
import pandas as pd

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eta_estimator.settings')
django.setup()

from estimator.models import Trade, Estimator

def get_trade(trade_name):
    """Get trade by name"""
    try:
        trade = Trade.objects.get(name=trade_name)
        return trade.id, trade.name
    except Trade.DoesNotExist:
        print(f"Failed to get trade with name: {trade_name}")
        return None, None

def create_estimator(trade_id, trade_name, index):
    """Create an estimator for a given trade."""
    try:
        estimator = Estimator.objects.create(
            name=f"Estimator - {trade_name} - {index}",
            email=f"estimator{index}@example.com",
            trade_id=trade_id
        )
        print(f"Created estimator: {estimator.name} for trade ID: {trade_id}")
        return True
    except Exception as e:
        print(f"Failed to create estimator: Estimator - {trade_name} - {index}, Error: {str(e)}")
        return False

def main():
    # Check if the CSV file exists
    if not os.path.exists('data_creation_assets/trades_info.csv'):
        print("Error: trades_info.csv not found!")
        return

    # Read the CSV file
    try:
        df = pd.read_csv('data_creation_assets/trades_info.csv', sep=';')
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return

    # Process each trade
    for _, row in df.iterrows():
        trade_name = row['Category - Requests']
        resource_count = int(row['Count of Resources'])

        # Get or create trade
        trade_id, trade_name = get_trade(trade_name)
        if not trade_id:
            continue

        # Create estimators for this trade
        for i in range(resource_count):
            create_estimator(trade_id, trade_name, i + 1)

if __name__ == "__main__":
    main() 