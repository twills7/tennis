import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import numpy as np

# match_data_2000 = pd.read_csv('year_stats/2000')
# match_data_2001 = pd.read_csv('year_stats/2001')
# match_data_2002 = pd.read_csv('year_stats/2002')
# match_data_2003 = pd.read_csv('year_stats/2003')
# match_data_2004 = pd.read_csv('year_stats/2004')
# match_data_2005 = pd.read_csv('year_stats/2005')
# match_data_2006 = pd.read_csv('year_stats/2006')
# match_data_2007 = pd.read_csv('year_stats/2007')
# match_data_2008 = pd.read_csv('year_stats/2008')
# match_data_2009 = pd.read_csv('year_stats/2009')
match_data_2010 = pd.read_csv('year_stats/2010')
match_data_2011 = pd.read_csv('year_stats/2011')
match_data_2012 = pd.read_csv('year_stats/2012')
match_data_2013 = pd.read_csv('year_stats/2013')
match_data_2014 = pd.read_csv('year_stats/2014')
match_data_2015 = pd.read_csv('year_stats/2015')
match_data_2016 = pd.read_csv('year_stats/2016')
match_data_2017 = pd.read_csv('year_stats/2017')
match_data_2018 = pd.read_csv('year_stats/2018')
match_data_2019 = pd.read_csv('year_stats/2019')
match_data_2020 = pd.read_csv('year_stats/2020')
match_data_2021 = pd.read_csv('year_stats/2021')
match_data_2022 = pd.read_csv('year_stats/2022')
match_data_2023 = pd.read_csv('year_stats/2023')
match_data_2024 = pd.read_csv('year_stats/2024')
match_data_2025 = pd.read_csv('year_stats/2025')

df = pd.concat([match_data_2010, match_data_2011, match_data_2012, match_data_2013, match_data_2014,
                        match_data_2015, match_data_2016, match_data_2017, match_data_2018, match_data_2019,
                        match_data_2020, match_data_2021, match_data_2022, match_data_2023, match_data_2024,
                        match_data_2025], ignore_index=True)


df = df.dropna(subset=["WRank", "LRank", "WPts", "LPts", "Winner", "Loser", "Surface", "Round"])

print(df.head())
df['rank_diff'] = df['WRank'] - df['LRank']
df['points_diff'] = df['WPts'] - df['LPts']
df['odds_diff'] = df['B365W'] - df['B365L']

# Create winner's view
winner_df = df.copy()
winner_df['player1'] = df['Winner']
winner_df['player2'] = df['Loser']
winner_df['rank_diff'] = df['WRank'] - df['LRank']
winner_df['points_diff'] = df['WPts'] - df['LPts']
winner_df['odds_diff'] = df['B365W'] - df['B365L']
winner_df['avg_odds_diff'] = df['AvgW'] - df['AvgL']
winner_df['best_of_5'] = (df['Best of'] == 5).astype(int)
winner_df['target'] = 1

loser_df = df.copy()
loser_df['player1'] = df['Loser']
loser_df['player2'] = df['Winner']
loser_df['rank_diff'] = df['LRank'] - df['WRank']
loser_df['points_diff'] = df['LPts'] - df['WPts']
loser_df['odds_diff'] = df['B365L'] - df['B365W']
loser_df['avg_odds_diff'] = df['AvgL'] - df['AvgW']
loser_df['best_of_5'] = (df['Best of'] == 5).astype(int)
loser_df['target'] = 0

# Combine them
final_df = pd.concat([winner_df, loser_df], ignore_index=True)

final_df = pd.get_dummies(final_df, columns=["Surface", "Round", "Series"], drop_first=True)

# 2. Make sure date is parsed properly
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# 3. Sort by most recent match first
df = df.sort_values('Date', ascending=False)

# Build latest player stats
player_to_rank = {}
player_to_avgW = {}
player_to_avgL = {}

# We'll use latest available match per player
for idx, row in df.iterrows():
    winner = row['Winner']
    loser = row['Loser']
    
    # Update winner's stats
    player_to_rank[winner] = row['WRank']
    player_to_avgW[winner] = row['AvgW']
    player_to_avgL[winner] = row['AvgL']
    
    # Update loser's stats
    player_to_rank[loser] = row['LRank']
    player_to_avgW[loser] = row['AvgW']
    player_to_avgL[loser] = row['AvgL']

features = [
    "rank_diff", "points_diff", "odds_diff", "avg_odds_diff", "best_of_5"
] + [col for col in final_df.columns if col.startswith("Surface_") or col.startswith("Series_")]

X = final_df[features]
y = final_df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)



model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(y_train.value_counts())
preds = model.predict(X_test)
probs = model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, preds))
print("AUC:", roc_auc_score(y_test, probs))



example_match = {
    "rank_diff": 12 - 8,
    "points_diff": 2000 - 2300,
    "odds_diff": 1.80 - 2.10,
    "Surface_Grass": 0,
    "Surface_Hard": 1,
    # other dummy values...
}

def create_match_features(player1, player2, player_to_rank, player_to_avgW, player_to_avgL, surface="Hard", round_name="R32", series="ATP250", best_of=3):
    features = {}
    
    # Basic diffs
    features["rank_diff"] = player_to_rank.get(player1, 1500) - player_to_rank.get(player2, 1500)
    features["points_diff"] = 0  # You could add points later too
    features["odds_diff"] = player_to_avgW.get(player1, 2.0) - player_to_avgW.get(player2, 2.0)
    features["avg_odds_diff"] = player_to_avgW.get(player1, 2.0) - player_to_avgL.get(player2, 2.0)
    features["best_of_5"] = 1 if best_of == 5 else 0

    # One-hot surfaces and rounds
    for s in ["Grass", "Hard"]:
        features[f"Surface_{s}"] = 1 if surface == s else 0

    for ser in ["ATP500","Grand Slam", "Masters 1000", "Masters Cup"]:
        features[f"Series_{ser}"] = 1 if series == ser else 0
    
    return pd.DataFrame([features])

player1 = "Bublik A."
player2 = "Mensik J."

# Build the feature vector automatically
match_features = create_match_features(player1, player2, player_to_rank, player_to_avgW, player_to_avgL, surface="Hard", round_name="QF", series="Grand Slam", best_of=3)

# Predict
pred = model.predict(match_features)[0]
prob = model.predict_proba(match_features)[0][1]

print(f"Prediction: {player1} wins" if pred == 1 else f"{player2} wins")
print(f"Probability that {player1} wins: {prob*100:.2f}%")