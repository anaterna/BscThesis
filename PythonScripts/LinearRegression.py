import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the data from the CSV file
data = pd.read_csv("./instance_grime_questdb.csv")

# Prepare data
X = data['TD'].values.reshape(-1,1) # independent variable
y = data['cg-na'].values.reshape(-1,1) # dependent variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create a linear regression model
model = LinearRegression() 

# Train the model using the training data
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Create scatter plot with regression line
sns.set(style="darkgrid")
plt.figure(figsize=(10, 6))
sns.scatterplot(x="TD", y="cg-na", data=data, label='Data Points')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Regression Line')
plt.title("Correlation between Grime (cg-na) and TD instances \n Case Ib: classes with unique grime instances, inter")
plt.ylabel("TD")
plt.xlabel("Grime: cg-na")

plt.legend()
#plt.savefig(f'FINAL_JHOT/case8.png', dpi=300)

plt.show()

