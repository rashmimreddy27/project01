import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Sample training data
data = {
    "Issue": [
        "Pothole", "Pothole", "Pothole",
        "Garbage", "Garbage", "Garbage",
        "Water Leakage", "Water Leakage",
        "Broken Streetlights", "Broken Streetlights"
    ],
    "Severity": [
        "High", "Medium", "Low",
        "High", "Medium", "Low",
        "High", "Low",
        "High", "Low"
    ],
    "Priority": [
        "Urgent", "Medium", "Low",
        "Urgent", "Medium", "Low",
        "Urgent", "Low",
        "Urgent", "Low"
    ]
}

# Convert data into a table
df = pd.DataFrame(data)

# Convert text into numbers
X = pd.get_dummies(df[["Issue", "Severity"]])
y = df["Priority"]

# Train the AI model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

print("AI model trained successfully!")

# Test the model
new_issue = pd.DataFrame({
    "Issue": ["Pothole"],
    "Severity": ["High"]
})

new_issue_encoded = pd.get_dummies(
    new_issue
).reindex(columns=X.columns, fill_value=0)

prediction = model.predict(new_issue_encoded)

print("Issue:", new_issue["Issue"][0])
print("Severity:", new_issue["Severity"][0])
print("Predicted Priority:", prediction[0])
