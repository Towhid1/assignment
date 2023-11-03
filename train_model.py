"""
Script to train model
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from download_data import FORECAST_TEMP_DIR
import joblib

MODEL_DIR = "model/RandomForestRegressor.joblib"


def main():
    """
    Main function to train a RandomForestRegressor model on temperature data and save the model.

    This function reads temperature data from a CSV file, extracts relevant features,
    splits the data into training and testing sets, trains a RandomForestRegressor model,
    evaluates the model on the testing set, and saves the trained model.

    Returns:
    - None
    """
    # Read temperature data from CSV file
    df = pd.read_csv(FORECAST_TEMP_DIR)

    # Convert the 'time' column to datetime type
    df['time'] = pd.to_datetime(df['time'])

    # Extracting numerical features from the date (e.g., day of the year)
    df['day_of_year'] = df['time'].dt.dayofyear
    df['day_of_week'] = df['time'].dt.day_of_week
    df['days_in_month'] = df['time'].dt.days_in_month
    df['month'] = df['time'].dt.month
    df['year'] = df['time'].dt.year

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        df[['day_of_year', 'day_of_week', 'month', 'days_in_month', 'year']], df['temperature_2m'],
        test_size=0.2, random_state=42)

    # Creating and training the RandomForestRegressor model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Save the trained model to a file
    joblib.dump(model, MODEL_DIR)

    # Evaluate the model on the testing set
    mae = mean_absolute_error(y_test, model.predict(X_test))
    print(f"Mean Absolute Error: {mae} °C")


if __name__ == '__main__':
    main()
