import pandas as pd
import os

FILE = "history.csv"

def save_prediction(entry):
    try:
        if os.path.exists(FILE):
            df = pd.read_csv(FILE)
            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        else:
            df = pd.DataFrame([entry])

        df.to_csv(FILE, index=False)

    except Exception as e:
        print("Error saving prediction:", e)


def load_history():
    try:
        if os.path.exists(FILE):
            df = pd.read_csv(FILE)

            # ✅ Ensure correct structure (prevents crashes)
            expected_cols = ["studytime", "failures", "absences", "health", "risk", "prob"]
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = None

            return df

        return pd.DataFrame(columns=["studytime", "failures", "absences", "health", "risk", "prob"])

    except Exception as e:
        print("Error loading history:", e)
        return pd.DataFrame(columns=["studytime", "failures", "absences", "health", "risk", "prob"])