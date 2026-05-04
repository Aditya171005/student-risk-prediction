import pandas as pd
import pickle

df = pd.read_csv("student_data.csv")

df['risk'] = df['G3'].apply(lambda x: 1 if x < 10 else 0)

X = df[["studytime", "failures", "absences", "health"]]
y = df['risk']

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

pickle.dump(model, open("model.pkl", "wb"))

print("✅ NEW model.pkl created")