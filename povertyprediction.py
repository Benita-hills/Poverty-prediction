# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def load_and_preprocess_data(file_path):
    # Your code for loading and processing the data
    df = pd.read_excel(file_path)
    # Continue with the rest of the preprocessing logic
    return df

file_path = "/content/5000 poverty rprediction.xlsx"
df = load_and_preprocess_data(file_path)

print(df.isnull().sum())

# Replace all non-numeric values (like '-') with NaN (Not a Number)
df.replace('-', np.nan, inplace=True)

# Convert the column to numeric, forcing any non-numeric values to NaN
df = df.apply(pd.to_numeric, errors='coerce')

# After replacement, handle missing values using the median (or any other method)
df.fillna(df.median(), inplace=True)

def detect_outliers_iqr(df, feature):
    # Calculate the Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[feature].quantile(0.25)
    Q3 = df[feature].quantile(0.75)

    # Calculate the Interquartile Range (IQR)
    IQR = Q3 - Q1

    # Calculate the lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Return a boolean series that marks outliers (True for outliers)
    return (df[feature] < lower_bound) | (df[feature] > upper_bound)

# Apply the IQR outlier detection for all numerical columns in the dataset
numerical_columns = df.select_dtypes(include=[np.number]).columns

outliers = pd.DataFrame()

for col in numerical_columns:
    outliers[col] = detect_outliers_iqr(df, col)

# Display rows where there are outliers
outlier_rows = df[outliers.any(axis=1)]
print("\nOutlier rows detected:")
print(outlier_rows)

# Count of outliers in each column
print("\nCount of outliers in each column:")
print(outliers.sum())

# Remove rows with outliers
df_cleaned = df[~outliers.any(axis=1)]  # ~ is the negation operator (to remove outliers)

# Display cleaned data
print("\nCleaned Data without Outliers:")
print(df_cleaned.head())

# Define the poverty line threshold
poverty_line = 137430  # Define the poverty line

#Classify house hold as poor (1) and non Poor(0) based on total consumption per capital
df['poor'] = (df["Consumption per capita"] < poverty_line).astype(int)

# Select relevant features for predicting poverty
X=df[['hhsize', 'Income source', 'Educational Level', 'Spending on food Items', 'Spending on non food items']]
y=df['poor']

# Correct the feature list by removing the trailing comma
X = df[['hhsize', 'Income source', 'Educational Level', 'Spending on food Items', 'Spending on non food items']]

# Step 4: Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train the model (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 6: Evaluate the model performance
y_pred = model.predict(X_test)

# Calculate performance metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Model Evaluation:")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print("Confusion Matrix:")
print(conf_matrix)

def get_user_input_and_predict():
    # Accept user input for relevant features
    print("\nEnter the details of the household to predict the poverty:")
    hhsize = int(input("Enter household size: "))  # Collect input for household size
    income_source = int(input("Enter income source (numeric value): "))  # Collect input for income source
    educational_level = int(input("Enter educational level (numeric value): "))  # Collect input for education level
    spending_food = float(input("Enter spending on food items: "))  # Collect input for food spending
    spending_non_food = float(input("Enter spending on non-food items: "))  # Collect input for non-food spending
    return pd.DataFrame([[hhsize, income_source, educational_level, spending_food, spending_non_food]],
                        columns=['hhsize', 'Income source', 'Educational Level', 'Spending on food Items', 'Spending on non food items'])

user_input = get_user_input_and_predict()

print(user_input)

# Predict using the trained model
def predict_poverty(user_input):
    prediction = model.predict(user_input)
    prediction = prediction[0]
    print(prediction)
    if prediction == 1:
        print("The household is predicted to be BELOW the poverty line (Poor).")
    else:
        print("The household is predicted to be ABOVE the poverty line (Not Poor).")

predict_poverty(user_input)
