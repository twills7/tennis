import pandas as pd

# Load your CSV data
y_2000 = pd.read_csv("year_stats/2000")
y_2001 = pd.read_csv("year_stats/2001")
y_2002 = pd.read_csv("year_stats/2002")
y_2003 = pd.read_csv("year_stats/2003")
y_2004 = pd.read_csv("year_stats/2004")
y_2005 = pd.read_csv("year_stats/2005")
y_2006 = pd.read_csv("year_stats/2006")
y_2007 = pd.read_csv("year_stats/2007")
y_2008 = pd.read_csv("year_stats/2008")
y_2009 = pd.read_csv("year_stats/2009")
y_2010 = pd.read_csv("year_stats/2010")
y_2011 = pd.read_csv("year_stats/2011")
y_2012 = pd.read_csv("year_stats/2012")
y_2013 = pd.read_csv("year_stats/2013")
y_2014 = pd.read_csv("year_stats/2014")
y_2015 = pd.read_csv("year_stats/2015")
y_2016 = pd.read_csv("year_stats/2016")
y_2017 = pd.read_csv("year_stats/2017")
y_2018 = pd.read_csv("year_stats/2018")
y_2019 = pd.read_csv("year_stats/2019")
y_2020 = pd.read_csv("year_stats/2020")
y_2021 = pd.read_csv("year_stats/2021")
y_2022 = pd.read_csv("year_stats/2022")
y_2023 = pd.read_csv("year_stats/2023")
y_2024 = pd.read_csv("year_stats/2024")
y_2025 = pd.read_csv("year_stats/2025")
# Combine all dataframes into one
matches_df = pd.concat([y_2000, y_2001, y_2002, y_2003, y_2004, y_2005, y_2006, y_2007,
                       y_2008, y_2009, y_2010, y_2011, y_2012, y_2013, y_2014, y_2015,
                       y_2016, y_2017, y_2018, y_2019, y_2020, y_2021, y_2022, y_2023,
                       y_2024, y_2025], ignore_index=True)

players = []

# get names from the year_stats folder and sort
def get_names(file_name):
    names = []
    with open(file_name, "r") as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip().split(",")
        if len(line) > 10 and "Winner" not in line:
            for player in [line[10], line[11]]:
                if player not in names:
                    names.append(player.lower().strip())
    names.sort()
    return names

# get all names from the year_stats folder and sort
def get_all_names():
    names = []
    for i in range(2000, 2026):
        file_name = f"year_stats/{i}"
        names += get_names(file_name)
    names = list(set(names))
    names = sorted(set(names))
    return names

def create_csv():
    with open("all_names.csv", "w") as file:
        for name in get_all_names():
            file.write(f"{name}\n")

import pandas as pd
from collections import defaultdict

def build_feature_dataset(matches_df):
    """
    Build a feature-rich dataset for tennis match prediction.
    
    Args:
        matches_df (pd.DataFrame): DataFrame with match results. Columns must include:
            - 'date', 'player_1', 'player_2', 'winner', 'surface', 'tournament', 'round',
              'rank_1', 'rank_2', (optional Elo or any base stats)
    
    Returns:
        pd.DataFrame: Feature-engineered dataset.
    """
    # Initialize player history dict
    player_stats = defaultdict(lambda: {
        'elo': 1500,  # base Elo
        'elo_surface': defaultdict(lambda: 1500),
        'matches_played': 0,
        'wins': 0,
        'surface_wins': defaultdict(int),
        'surface_matches': defaultdict(int),
        'recent_results': [],  # store last 5 outcomes (1/0)
    })
    
    feature_rows = []

    for _, row in matches_df.sort_values('Date').iterrows():
        p1 = row['Winner']
        p2 = row['Loser']
        winner = row['Winner']
        surface = row['Surface']

        # Get current stats
        p1_stats = player_stats[p1]
        p2_stats = player_stats[p2]

        # Derived stats
        p1_win_pct = (p1_stats['wins'] / p1_stats['matches_played']) if p1_stats['matches_played'] > 0 else 0.5
        p2_win_pct = (p2_stats['wins'] / p2_stats['matches_played']) if p2_stats['matches_played'] > 0 else 0.5

        p1_surface_win_pct = (p1_stats['surface_wins'][surface] / p1_stats['surface_matches'][surface]) if p1_stats['surface_matches'][surface] > 0 else 0.5
        p2_surface_win_pct = (p2_stats['surface_wins'][surface] / p2_stats['surface_matches'][surface]) if p2_stats['surface_matches'][surface] > 0 else 0.5

        # Recent form (last 5 matches)
        p1_recent_wins = sum(p1_stats['recent_results'][-5:]) if p1_stats['recent_results'] else 0
        p2_recent_wins = sum(p2_stats['recent_results'][-5:]) if p2_stats['recent_results'] else 0

        # Head-to-head record (simple wins count)
        h2h_key = tuple(sorted([p1, p2]))
        if 'h2h' not in player_stats:
            player_stats['h2h'] = defaultdict(lambda: {'wins': defaultdict(int)})
        p1_h2h_wins = player_stats['h2h'][h2h_key]['wins'][p1]
        p2_h2h_wins = player_stats['h2h'][h2h_key]['wins'][p2]

        # Rank diff (optional: you can pull from your dataset if you have real-time ranks)
        if row['WRank'] not in ['NR', None, '']:
            rank_1 = float(row['WRank'])
        else:
            rank_1 = 999
        if row['LRank'] not in ['NR', None, '']:
            rank_2 = float(row['LRank'])
        else:
            rank_2 = 999
        rank_diff = rank_1 - rank_2

        # Elo diff
        elo_diff = p1_stats['elo'] - p2_stats['elo']
        elo_surface_diff = p1_stats['elo_surface'][surface] - p2_stats['elo_surface'][surface]

        # Assemble the feature row
        feature_rows.append({
            'date': row['Date'],
            'player_1': p1,
            'player_2': p2,
            'surface': surface,
            'tournament': row['Tournament'],
            'round': row['Round'],
            'winner': 1 if winner == p1 else 0,

            'rank_1': row['WRank'],
            'rank_2': row['LRank'],
            'rank_diff': rank_diff,

            'elo_1': p1_stats['elo'],
            'elo_2': p2_stats['elo'],
            'elo_diff': elo_diff,

            'elo_surface_1': p1_stats['elo_surface'][surface],
            'elo_surface_2': p2_stats['elo_surface'][surface],
            'elo_surface_diff': elo_surface_diff,

            'win_pct_1': p1_win_pct,
            'win_pct_2': p2_win_pct,
            'win_pct_diff': p1_win_pct - p2_win_pct,

            'surface_win_pct_1': p1_surface_win_pct,
            'surface_win_pct_2': p2_surface_win_pct,
            'surface_win_pct_diff': p1_surface_win_pct - p2_surface_win_pct,

            'recent_wins_1': p1_recent_wins,
            'recent_wins_2': p2_recent_wins,
            'recent_wins_diff': p1_recent_wins - p2_recent_wins,

            'h2h_wins_1': p1_h2h_wins,
            'h2h_wins_2': p2_h2h_wins,
            'h2h_diff': p1_h2h_wins - p2_h2h_wins,
        })

        # 🔄 Update player stats after match
        for player, is_winner in [(p1, winner == p1), (p2, winner == p2)]:
            stats = player_stats[player]
            stats['matches_played'] += 1
            stats['surface_matches'][surface] += 1
            if is_winner:
                stats['wins'] += 1
                stats['surface_wins'][surface] += 1
            stats['recent_results'].append(1 if is_winner else 0)
            # Limit recent results to 20 max
            if len(stats['recent_results']) > 20:
                stats['recent_results'] = stats['recent_results'][-20:]

        # Update head-to-head
        player_stats['h2h'][h2h_key]['wins'][winner] += 1

        # ➕ Elo update (basic; tweak as needed)
        K = 32  # can tune this
        expected_p1 = 1 / (1 + 10 ** ((p2_stats['elo'] - p1_stats['elo']) / 400))
        expected_p2 = 1 - expected_p1
        score_p1 = 1 if winner == p1 else 0
        score_p2 = 1 - score_p1

        p1_stats['elo'] += K * (score_p1 - expected_p1)
        p2_stats['elo'] += K * (score_p2 - expected_p2)

        # Surface-specific Elo update
        expected_p1_surf = 1 / (1 + 10 ** ((p2_stats['elo_surface'][surface] - p1_stats['elo_surface'][surface]) / 400))
        expected_p2_surf = 1 - expected_p1_surf
        p1_stats['elo_surface'][surface] += K * (score_p1 - expected_p1_surf)
        p2_stats['elo_surface'][surface] += K * (score_p2 - expected_p2_surf)

    # Final DataFrame
    return pd.DataFrame(feature_rows)

if __name__ == "__main__":
    # Create CSV with all player names
    create_csv()

    # Build the feature dataset
    feature_dataset = build_feature_dataset(matches_df)

    # Save to CSV
    feature_dataset.to_csv("feature_dataset.csv", index=False)