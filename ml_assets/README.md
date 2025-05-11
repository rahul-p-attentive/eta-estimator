# ML Assets Directory

This directory contains the machine learning model and associated files used for time estimation.

## Required Files

1. `model_epoch25_valmae0.0005.keras` - The trained Keras model
2. `workable_sheets_count_scaler.pkl` - Scaler for workable sheets count
3. `y_scaler.pkl` - Scaler for the target variable (time)
4. `columns.pkl` - List of feature columns used in the model

## File Descriptions

- **model_epoch25_valmae0.0005.keras**: The trained neural network model that predicts time based on trade estimations.
- **workable_sheets_count_scaler.pkl**: Scaler used to normalize the workable sheets count input.
- **y_scaler.pkl**: Scaler used to denormalize the model's output back to actual time values.
- **columns.pkl**: List of column names that defines the order and structure of input features.

## Usage

These files are automatically loaded by the `MLTimePredictor` class when the application starts. Make sure all files are present in this directory for the time estimation feature to work properly. 