import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os

# 1. Setup Paths (Using the folders I saw in your screenshot)
# We use os.path.join to be safe on Linux
data_path = os.path.join('Data', 'diabetes.csv')
model_path = os.path.join('Models', 'twin_brain.pkl')

# Check if data exists
if not os.path.exists(data_path):
    print(f" Error: Could not find {data_path}")
    print("Please make sure 'diabetes.csv' is inside the 'Data' folder.")
    exit()

# 2. Load Data
print("Loading data...")
df = pd.read_csv(data_path)

# 3. Clean Data 
# (Replacing 0s with NaN for columns where 0 is medically impossible)
print("Cleaning data...")
cols_to_fix = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in cols_to_fix:
    df[col] = df[col].replace(0, pd.NA)
    df[col] = df[col].fillna(df[col].mean())

# 4. Train Model
print("Training AI model...")
X = df.drop('Outcome', axis=1)
y = df['Outcome']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Check Accuracy
acc = accuracy_score(y_test, model.predict(X_test))
print(f"Model Trained! Accuracy: {acc*100:.2f}%")

# 6. Save the 'Brain' inside the Models folder
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
print(f"Brain saved successfully at: {model_path}")