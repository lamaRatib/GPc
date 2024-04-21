import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import LeaveOneOut


import db
import plotly.express as px


sql = """
    SELECT DATE_FORMAT(date, '%Y-%m') AS month,
           SUM(discounted_price) AS total_sales
    FROM sales
    GROUP BY DATE_FORMAT(date, '%Y-%m')
    ORDER BY DATE_FORMAT(date, '%Y-%m');
"""
data = db.DB().query(sql)
df=pd.DataFrame(data)
df[0] = pd.to_datetime(df[0])
df['Month'] = df[0].dt.month
df['Year'] = df[0].dt.year
X = df[['Month', 'Year']].values
y = df[1].values

# Define the degrees for polynomial regression
degrees = [2, 3, 4, 5, 6]

# Initialize models
models = {
    "Polynomial Regression (degree 2)": LinearRegression(),
    "Polynomial Regression (degree 3)": LinearRegression(),
    "Polynomial Regression (degree 4)": LinearRegression(),
    "Polynomial Regression (degree 5)": LinearRegression(),
    "Polynomial Regression (degree 6)": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
}

# Initialize k-fold cross-validation
loo = LeaveOneOut()

# Initialize dictionary to store performance metrics
mse_scores = {model_name: [] for model_name in models}

# Perform k-fold cross-validation
for train_index, test_index in loo.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    for model_name, model in models.items():
        if "Polynomial" in model_name:
            degree = int(model_name.split()[-1][:-1])
            poly_features = PolynomialFeatures(degree=degree)
            X_train_poly = poly_features.fit_transform(X_train)
            model.fit(X_train_poly, y_train)
            X_test_poly = poly_features.transform(X_test)
            y_pred = model.predict(X_test_poly)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        mse_scores[model_name].append(mse)

# Calculate average performance metrics
average_mse = {model_name: np.mean(scores) for model_name, scores in mse_scores.items()}
for model_name, mse in average_mse.items():
    print(f"Average MSE for {model_name}: {mse}")