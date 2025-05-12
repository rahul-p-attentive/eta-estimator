from collections import defaultdict
import os
import pickle
from tensorflow import keras
from keras.models import load_model
import numpy as np
import pandas as pd
from datetime import datetime

class MLTimePredictor:
    def __init__(self):
        self.model = None
        self.workable_sheets_count_scaler = None
        self.y_scaler = None
        self.columns = None
        self.expected_columns = ['construction_request_id', 'trade_name', 'workable_sheets_count', 'start_time']
        self._load_model_and_scalers()

    def _load_model_and_scalers(self):
        """Load the ML model and scalers from the saved files."""
        try:
            # Get the base directory (project root)
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Construct paths to the model files
            model_path = os.path.join(base_dir, "ml_assets", "model_epoch25_valmae0.0005.keras")
            workable_scaler_path = os.path.join(base_dir, "ml_assets", "workable_sheets_count_scaler.pkl")
            y_scaler_path = os.path.join(base_dir, "ml_assets", "y_scaler.pkl")
            columns_path = os.path.join(base_dir, "ml_assets", "columns.pkl")

            # Load the model and scalers
            self.model = load_model(model_path)
            
            with open(workable_scaler_path, 'rb') as f:
                self.workable_sheets_count_scaler = pickle.load(f)
            
            with open(y_scaler_path, 'rb') as f:
                self.y_scaler = pickle.load(f)
            
            with open(columns_path, 'rb') as f:
                self.columns = pickle.load(f)

        except Exception as e:
            raise Exception(f"Error loading ML model and scalers: {str(e)}")
    
    def prepare_X(self, data: pd.DataFrame):
        data_new = pd.get_dummies(data, columns=['trade_name'], drop_first=True, dtype=float)
        data_new = data_new.reindex(columns=self.columns, fill_value=0.0)
        
        data_new['start_time'] = pd.to_datetime(data_new['start_time']).dt.tz_localize(None)
        
        data_new['hour_sin'] = np.sin(2 * np.pi * data_new['start_time'].dt.hour / 24)
        data_new['hour_cos'] = np.cos(2 * np.pi * data_new['start_time'].dt.hour / 24)
        
        data_new['day_of_week_sin'] = np.sin(2 * np.pi * data_new['start_time'].dt.dayofweek / 7)
        data_new['day_of_week_cos'] = np.cos(2 * np.pi * data_new['start_time'].dt.dayofweek / 7)
        
        data_new['day_of_year_sin'] = np.sin(2 * np.pi * data_new['start_time'].dt.dayofyear / 365)
        data_new['day_of_year_cos'] = np.cos(2 * np.pi * data_new['start_time'].dt.dayofyear / 365)
        
        data_new['is_weekend'] = data_new['start_time'].dt.dayofweek.isin([5, 6]).astype(float)
        
        data_new = data_new.drop(columns=['start_time'])

        if "construction_request_id" in data_new.columns:
            data_new = data_new.drop(columns=['construction_request_id'])
        
        if "time_taken" in data_new.columns:
            data_new = data_new.drop(columns=['time_taken'])

        data_new['workable_sheets_count'] = self.workable_sheets_count_scaler.transform(data_new['workable_sheets_count'].values.reshape(-1, 1)).reshape(-1)

        return data_new
    
    def scale_out_y(self, ys: np.array):
        return self.y_scaler.inverse_transform(ys)
    
    def get_trade_count_map(self, user_input):
        trade_count_map = defaultdict(int)
        for trade in user_input:
            if trade['is_workable']:
                for trade_name in trade['trades']:
                    trade_count_map[trade_name] += 1
        
        return trade_count_map
    
    def get_dataframe(self, trade_count_map, construction_request_id):
        """
            Counts the number of workable sheets for each trade and returns a dataframe with multiple rows for each trade.
            Fields that will be present in the dataframe are:
            - construction_request_id: The id of the construction request
            - trade_name: The name of the trade
            - workable_sheets_count: The number of workable sheets for the trade
            - start_time: The current time
        """
        data = pd.DataFrame(columns=self.expected_columns)
        
        for trade_name, count in trade_count_map.items():
            data = data._append({
                'construction_request_id': construction_request_id,
                'trade_name': trade_name,
                'workable_sheets_count': count,
                'start_time': datetime.now()
            }, ignore_index=True)
        return data

    def predict_estimated_times(self, user_input, construction_request_id=None):
        """
        Predict the time based on trade estimations.
        
        Args:
            construction_request_id (int): The id of the construction request
            user_input (dict): Dictionary containing trade information
                Each dict should have:
                - is_workable (bool): Whether the trade is workable
                - trades (list): List of trade names
        
        Returns:
            dict: Predicted time for each trade
        """
        try:
            trade_count_map = self.get_trade_count_map(user_input)
            data = self.get_dataframe(trade_count_map, construction_request_id)
            trade_names = data['trade_name'].values
            data = self.prepare_X(data)
            ys = self.model.predict(data)
            ys = self.scale_out_y(ys)

            return dict(zip(trade_names, ys.reshape(-1)))
            
        except Exception as e:
            raise Exception(f"Error making prediction: {str(e)}")

# Create a singleton instance
time_predictor = MLTimePredictor() 