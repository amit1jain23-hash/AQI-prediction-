import pandas as pd
from sklearn.linear_model import LinearRegression

# Sample data
data = pd.DataFrame({
    'pm25': [50, 30, 100],
    'pm10': [80, 60, 150],
    'aqi': [120, 90, 200]
})

X = data[['pm25', 'pm10']]
y = data['aqi']

model = LinearRegression()
model.fit(X, y)

# Test prediction
print(model.predict([[60, 90]]))