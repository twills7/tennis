import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss, classification_report
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

import numpy as np

# Load your feature dataset
df = pd.read_csv("feature_dataset.csv")

# Randomly flip 50% of rows
flip_mask = np.random.rand(len(df)) < 0.5

# Identify the columns that need to be swapped (all _1 and _2)
feature_cols = [col for col in df.columns if '_1' in col or '_2' in col]
pair_cols = set(col.replace('_1', '') for col in feature_cols if '_1' in col)

for base in pair_cols:
    col1 = f"{base}_1"
    col2 = f"{base}_2"
    # Swap these two columns where flip_mask is True
    df.loc[flip_mask, [col1, col2]] = df.loc[flip_mask, [col2, col1]].values

# Flip the winner label
df.loc[flip_mask, 'winner'] = 1 - df.loc[flip_mask, 'winner']

# Optional sanity check
print(df['winner'].value_counts())


# Set target & features
y = df['winner']
X = df.drop(columns=['date', 'player_1', 'player_2', 'surface', 'tournament', 'round', 'winner'])

print("Class distribution (whole dataset):")
print(df['winner'].value_counts())
df.fillna(999, inplace=True)  # Fill NaN values with 999

# Train/test split (time-based is better, but random is ok for now to benchmark)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.fillna(999, inplace=True)  # Fill NaN values with 999
X_test.fillna(999, inplace=True)  # Fill NaN values with 999

print("\nClass distribution (train set):")
print(y_train.value_counts())

print("\nClass distribution (test set):")
print(y_test.value_counts())

# 1️⃣ Logistic Regression (baseline)
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)
log_preds = logreg.predict(X_test)
log_proba = logreg.predict_proba(X_test)

print("\n=== Logistic Regression ===")
print("Accuracy:", accuracy_score(y_test, log_preds))
print("Log Loss:", log_loss(y_test, log_proba))
print(classification_report(y_test, log_preds))

# 2️⃣ XGBoost Classifier
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb.fit(X_train, y_train)
xgb_preds = xgb.predict(X_test)
xgb_proba = xgb.predict_proba(X_test)

print("\n=== XGBoost ===")
print("Accuracy:", accuracy_score(y_test, xgb_preds))
print("Log Loss:", log_loss(y_test, xgb_proba))
print(classification_report(y_test, xgb_preds))

# from xgboost import plot_importance
# import matplotlib.pyplot as plt

# plot_importance(xgb)
# plt.show()

rank_1 = input("Enter rank for Player 1: ")
rank_2 = input("Enter rank for Player 2: ")
rank_diff = int(rank_1) - int(rank_2)

elo_1 = input("Enter Elo rating for Player 1: ")
elo_2 = input("Enter Elo rating for Player 2: ")
elo_diff = int(elo_1) - int(elo_2)

elo_surface_1 = input("Enter Elo rating for Player 1 on the surface: ")
elo_surface_2 = input("Enter Elo rating for Player 2 on the surface: ")
elo_surface_diff = int(elo_surface_1) - int(elo_surface_2)

win_pct_1 = input("Enter win percentage for Player 1: ")
win_pct_2 = input("Enter win percentage for Player 2: ")
win_pct_diff = float(win_pct_1) - float(win_pct_2)

surface_win_pct_1 = input("Enter surface win percentage for Player 1: ")
surface_win_pct_2 = input("Enter surface win percentage for Player 2: ")
surface_win_pct_diff = float(surface_win_pct_1) - float(surface_win_pct_2)

recent_wins_1 = input("Enter recent wins for Player 1: ")
recent_wins_2 = input("Enter recent wins for Player 2: ")
recent_wins_diff = int(recent_wins_1) - int(recent_wins_2)

h2h_wins_1 = input("Enter H2H wins for Player 1: ")
h2h_wins_2 = input("Enter H2H wins for Player 2: ")
h2h_diff = int(h2h_wins_1) - int(h2h_wins_2)
surface = input("Enter surface type (e.g., 'hard', 'clay', 'grass'): ")

# Create a DataFrame for the new match
new_match = {
    'rank_1': int(rank_1),
    'rank_2': int(rank_2),
    'rank_diff': rank_diff,
    'elo_1': int(elo_1),
    'elo_2': int(elo_2),
    'elo_diff': elo_diff,
    'elo_surface_1': int(elo_surface_1),
    'elo_surface_2': int(elo_surface_2),
    'elo_surface_diff': elo_surface_diff,
    'win_pct_1': float(win_pct_1),
    'win_pct_2': float(win_pct_2),
    'win_pct_diff': win_pct_diff,
    'surface_win_pct_1': float(surface_win_pct_1),
    'surface_win_pct_2': float(surface_win_pct_2),
    'surface_win_pct_diff': surface_win_pct_diff,
    'recent_wins_1': int(recent_wins_1),
    'recent_wins_2': int(recent_wins_2),
    'recent_wins_diff': recent_wins_diff,
    'h2h_wins_1': int(h2h_wins_1),
    'h2h_wins_2': int(h2h_wins_2),
    'h2h_diff': h2h_diff
}

# new_match = {
#     'rank_1': 5,
#     'rank_2': 3,
#     'rank_diff': 5 - 3,

#     'elo_1': 2100,
#     'elo_2': 2150,
#     'elo_diff': 2100 - 2150,

#     'elo_surface_1': 2200,
#     'elo_surface_2': 2250,
#     'elo_surface_diff': 2200 - 2250,

#     'win_pct_1': 0.88,
#     'win_pct_2': 0.90,
#     'win_pct_diff': 0.88 - 0.90,

#     'surface_win_pct_1': 0.95,
#     'surface_win_pct_2': 0.92,
#     'surface_win_pct_diff': 0.95 - 0.92,

#     'recent_wins_1': 4,
#     'recent_wins_2': 5,
#     'recent_wins_diff': 4 - 5,

#     'h2h_wins_1': 2,
#     'h2h_wins_2': 3,
#     'h2h_diff': 2 - 3,
# }
X_new = pd.DataFrame([new_match])
X_new.fillna(999, inplace=True)  # Fill NaN values with 999

# Make predictions
logreg_pred = logreg.predict(X_new)
xgb_pred = xgb.predict(X_new)
logreg_proba = logreg.predict_proba(X_new)
xgb_proba = xgb.predict_proba(X_new)
print("\n=== Predictions for the new match ===")
print("Logistic Regression Prediction:", "Player 1" if logreg_pred[0] == 1 else "Player 2")
print("Logistic Regression Probability:", logreg_proba[0][1])
print("XGBoost Prediction:", "Player 1" if xgb_pred[0] == 1 else "Player 2")
print("XGBoost Probability:", xgb_proba[0][1])