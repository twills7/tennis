import os

class Elo:
    def __init__(self, base_elo=1500):
        self.base_elo = base_elo
        self.k_base = 250
        self.all_time = {}
        self.this_year = {}
        self.last_3 = {}
        self.surface_elo = {}
        self.matches = {}
        self.surface_matches = {}
        self.correct = 0
        self.incorrect = 0
        self.exp_corr = 0
        self.exp_incorr = 0

    def read_file(self, year):
        filepath = f"year_stats/{year}"
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'r') as f:
            return [line.split(',') for line in f.read().splitlines() if line.strip()]

    def initialize_players(self, year_data, target_dict):
        for game in year_data:
            if len(game) > 10 and "Winner" not in game:
                for player in [game[10], game[11]]:
                    if player not in target_dict:
                        target_dict[player] = self.base_elo

    def update_elo(self, winner, loser, ratings, match_counts=None):
        win_prob = 1 / (1 + 10 ** ((ratings[loser] - ratings[winner]) / 400))
        if match_counts:
            k_winner = self.k_base / ((match_counts.get(winner, 0) + 5) ** 0.4)
            k_loser = self.k_base / ((match_counts.get(loser, 0) + 5) ** 0.4)
        else:
            k_winner = k_loser = 32  # static K otherwise

        ratings[winner] += k_winner * (1 - win_prob)
        ratings[loser] += k_loser * (0 - (1 - win_prob))

        ratings[winner] = max(0, ratings[winner])
        ratings[loser] = max(0, ratings[loser])

    def process_year(self, year):
        data = self.read_file(year)
        self.initialize_players(data, self.all_time)

        for game in data:
            if len(game) > 10 and "Winner" not in game:
                winner, loser = game[10], game[11]
                self.update_elo(winner, loser, self.all_time)

    def last_3_years_elo(self, current_year):
        years = [current_year - 2, current_year - 1]
        for year in years:
            data = self.read_file(year)
            self.initialize_players(data, self.last_3)
            for game in data:
                if len(game) > 10 and "Winner" not in game:
                    winner, loser = game[10], game[11]
                    self.update_elo(winner, loser, self.last_3)

    def this_year_elo(self, year):
        data = self.read_file(year)
        self.initialize_players(data, self.this_year)

        for game in data:
            if len(game) > 10 and "Winner" not in game:
                winner, loser = game[10], game[11]

                if winner not in self.this_year:
                    self.this_year[winner] = self.last_3.get(winner, self.base_elo)
                if loser not in self.this_year:
                    self.this_year[loser] = self.last_3.get(loser, self.base_elo)

                self.matches[winner] = self.matches.get(winner, 0) + 1
                self.matches[loser] = self.matches.get(loser, 0) + 1

                self.predict_and_update(winner, loser, self.this_year, self.matches)

    def predict_and_update(self, winner, loser, ratings, match_counts):
        win_prob = 1 / (1 + 10 ** ((ratings[loser] - ratings[winner]) / 400))
        
        self.exp_corr += win_prob
        self.exp_incorr += (1 - win_prob)

        # Only count if confident prediction
        prediction = winner if win_prob > 0.5 else loser
        if prediction == winner:
            self.correct += 1
        else:
            self.incorrect += 1

        self.update_elo(winner, loser, ratings, match_counts)

    def check_results(self):
        total = self.correct + self.incorrect
        if total > 0:
            acc = (self.correct / total) * 100
            exp_acc = (self.exp_corr / (self.exp_corr + self.exp_incorr)) * 100
            print(f"Correct Predictions: {self.correct}")
            print(f"Incorrect Predictions: {self.incorrect}")
            print(f"Accuracy: {acc:.2f}%")
            print(f"Expected Accuracy: {exp_acc:.2f}%")
        else:
            print("No confident predictions made yet.")

    def print_rankings(self, rating_dict):
        sorted_players = sorted(rating_dict.items(), key=lambda x: x[1], reverse=True)
        for i, (name, elo) in enumerate(sorted_players, 1):
            print(f"{i:<3} {name:<20} {int(elo):>5}")

def main(print_rankings=True, year=2025):
    tennis = Elo()

    tennis.process_year(year)  # example start
    tennis.last_3_years_elo(year)
    tennis.this_year_elo(year)
    if print_rankings:
        tennis.print_rankings(tennis.this_year)
    tennis.check_results()
    return tennis.correct, tennis.exp_corr, tennis.incorrect, tennis.exp_incorr

if __name__ == "__main__":
    main()