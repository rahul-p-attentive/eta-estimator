import os
import pickle
from tensorflow.keras.models import load_model
import numpy as np

class MLTimePredictor:
    def __init__(self):
        self.model = None
        self.workable_sheets_count_scaler = None
        self.y_scaler = None
        self.columns = None
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

    def predict_time(self, trade_estimations):
        """
        Predict the time based on trade estimations.
        
        Args:
            trade_estimations (list): List of dictionaries containing trade information
                Each dict should have:
                - is_workable (bool): Whether the trade is workable
                - trades (list): List of trade names
        
        Returns:
            float: Predicted time
        """
        try:
            # TODO: Implement the prediction logic here
            # 1. Process the trade_estimations into the format expected by the model
            # 2. Scale the input features using workable_sheets_count_scaler
            # 3. Make prediction using the model
            # 4. Inverse transform the prediction using y_scaler
            
            # Placeholder for now
            return 0.0
            
        except Exception as e:
            raise Exception(f"Error making prediction: {str(e)}")

# Create a singleton instance
time_predictor = MLTimePredictor() 