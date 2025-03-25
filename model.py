import numpy as np
import math
from scipy.stats import binom

class Model():

    def __init__(self, surface, name1, name2):
        self.name_1 = name1
        self.name_1_serve_WP = 0
        self.name_1_return_WP = 0
        self.name_1_tiebreak_WP = 0
        self.name_2 = name2
        self.name_2_serve_WP = 0
        self.name_2_return_WP = 0
        self.name_2_tiebreak_WP = 0
        self.serving_WP = [0, 0]
        self.surface = surface

    def get_surface_WP(self):
        service_file = "stats/" + self.surface + "_service_WP"
        return_file = "stats/" + self.surface + "_return_WP"
        tie_break_file = "stats/" + self.surface + "_tiebreak_WP"

        with open(service_file, 'r') as file:
            service_f = file.read()

        with open(return_file, 'r') as file:
            return_f = file.read()

        for line in service_f.split("\n"):
            if self.name_1 in line:
                serve_WP = line.split()[-1]
                self.name_1_serve_WP = float(serve_WP[:-1]) / 100
            elif self.name_2 in line:
                serve_WP = line.split()[-1]
                self.name_2_serve_WP = float(serve_WP[:-1]) / 100
        
        for line in return_f.split("\n"):
            if self.name_1 in line:
                return_WP = line.split()[-1]
                self.name_1_return_WP = float(return_WP[:-1]) / 100
            elif self.name_2 in line:
                return_WP = line.split()[-1]
                self.name_2_return_WP = float(return_WP[:-1]) / 100

        for line in tie_break_file.split("\n"):
            if self.name_1 in line:
                tiebreak_WP = line.split()[-1]
                self.name_1_tiebreak_WP = float(tiebreak_WP[:-1]) / 100
            elif self.name_2 in line:
                tiebreak_WP = line.split()[-1]
                self.name_2_tiebreak_WP = float(tiebreak_WP[:-1]) / 100
        if self.name_1_tiebreak_WP == 0:
            self.name_1_tiebreak_WP = 0.5
        if self.name_2_tiebreak_WP == 0:
            self.name_2_tiebreak_WP = 0.5
        self.name_1_tiebreak_WP = (self.name_1_tiebreak_WP + 0.5) / 2
        self.name_2_tiebreak_WP = (self.name_2_tiebreak_WP + 0.5) / 2

    def calculate_game_WP(self):
        name_1_game_serving_WP = self.name_1_serve_WP * (1 - self.name_2_return_WP)
        name_2_game__serving_WP = self.name_2_serve_WP * (1 - self.name_1_return_WP)
        self.serving_WP = [name_1_game_serving_WP, name_2_game__serving_WP]
        print(self.serving_WP)

    def win_game(self, prob_win_game):
        """Simulates a game and returns True if the server wins, False otherwise."""
        return np.random.rand() < prob_win_game

    def win_set(self, simulations=1000):
        """Simulates a set and returns the probability of Player 1 winning."""
        p1_wins = 0
        p1_game_win = self.serving_WP[0]
        p2_game_win = self.serving_WP[1]
        p1_tiebreak = self.name_1_tiebreak_WP
        p2_tiebreak = self.name_2_tiebreak_WP

        for _ in range(simulations):
            p1_games, p2_games = 0, 0
            while True:
                if (p1_games + p2_games) % 2 == 0:  # Player 1 serves
                    if self.win_game(p1_game_win):
                        p1_games += 1
                    else:
                        p2_games += 1
                else:  # Player 2 serves
                    if self.win_game(p2_game_win):
                        p2_games += 1
                    else:
                        p1_games += 1
                
                if p1_games >= 6 and p1_games - p2_games >= 2:
                    p1_wins += 1
                    break
                if p2_games >= 6 and p2_games - p1_games >= 2:
                    break
                
                if p1_games == 6 and p2_games == 6:  # Tiebreak
                    tiebreak = np.random.rand() < (p1_tiebreak + p2_tiebreak) / 2  # Assuming equal tiebreak odds
                    if tiebreak:
                        p1_wins += 1
                    break
                    
        return p1_wins / simulations
    
    def win_match(self, best_of=5, simulations=10000):
        """Simulates a match and returns the probability of Player 1 winning."""
        p1_game_win = self.serving_WP[0]
        p2_game_win = self.serving_WP[1]
        sets_needed = best_of // 2 + 1
        p1_wins = 0
        for _ in range(simulations):
            p1_sets, p2_sets = 0, 0
            while p1_sets < sets_needed and p2_sets < sets_needed:
                if self.win_set(simulations=1) > 0.5:
                    p1_sets += 1
                else:
                    p2_sets += 1
            
            if p1_sets >= sets_needed:
                p1_wins += 1
        
        return p1_wins / simulations
        

if __name__ == "__main__":
    surface = input("Enter surface: ")
    name1 = input("Enter name 1: ")
    name2 = input("Enter name 2: ")
    model = Model(surface, name1, name2)
    model.get_surface_WP()
    print(model.name_1_serve_WP)
    print(model.name_1_return_WP)
    print(model.name_2_serve_WP)
    print(model.name_2_return_WP)
    print(model.calculate_game_WP())
    print(model.win_set())
    print(name1 + " winning chance is " + str(model.win_match(simulations=10))+ " in 10 simulations")
    print(name1 + " winning chance is " + str(model.win_match(simulations=100)) + " in 100 simulations")
    print(name1 + " winning chance is " + str(model.win_match(simulations=1000)) + " in 1000 simulations")
    print(name1 + " winning chance is " + str(model.win_match(simulations=10000)) + " in 10000 simulations")
    print(name1 + " winning chance is " + str(model.win_match(simulations=100000)) + " in 100000 simulations")