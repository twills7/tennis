
class Elo():
    def __init__(self):
        self.name = ""
        self.surface = ""
        self.elo = 1200
        self.k = 32
        self.all_time = {}
        self.this_year = {}
        self.last_3 = {}

    def get_overall_elo(self, name):
        for year in range(2000, 2026):
            with open(f"year_stats/{year}", 'r') as file:
                elo_f = file.read()

            for line in elo_f.split("\n"):
                if self.name in line:
                    self.elo = float(line.split()[-1])
    
    def get_names(self):
        names = {}
        for year in range(2000, 2026):
            with open(f"year_stats/{year}", 'r') as file:
                elo_f = file.read()

            for line in elo_f.split("\n"):
                game = line.split(',')
                if len(game) > 10 and "Winner" not in game:
                    name1 = game[10]
                    name2 = game[11]
                    if name1 not in names:
                        names[name1] = 1500
                    if name2 not in names:
                        names[name2] = 1500
        with open("year_stats/names", 'w') as file:
            for name, elo in names.items():
                file.write(f"{name}, {elo}\n")

    def populate_elo(self):
        with open("year_stats/names", 'r') as file:
            elo_f = file.read()

        for line in elo_f.split("\n"):
            if line == "":
                continue
            name, elo = line.split(",")
            self.all_time[name] = float(elo)
    
    def to_string(self):
        self.all_time = dict(sorted(self.all_time.items(), key=lambda item: item[1], reverse=False))
        for name, elo in self.all_time.items():
            print(f"{name:<20} {int(elo):>5}")

    def year_to_string(self):
        self.this_year = dict(sorted(self.this_year.items(), key=lambda item: item[1], reverse=True))
        for name, elo in self.this_year.items():
            print(f"{name:<20} {int(elo):>5}")

    def update_elo(self, winner, loser):
        self.all_time[winner] += self.k * (1 - (1 / (1 + 10 ** ((self.all_time[winner] - self.all_time[loser]) / 400))))
        self.all_time[loser] += self.k * (0 - (1 / (1 + 10 ** ((self.all_time[loser] - self.all_time[winner]) / 400))))
        if self.all_time[winner] < 0:
            self.all_time[winner] = 0
        if self.all_time[loser] < 0:
            self.all_time[loser] = 0

    def update_elo_this_year(self, winner, loser, year):
        self.this_year[winner] += self.k * (1 - (1 / (1 + 10 ** ((self.this_year[winner] - self.this_year[loser]) / 400))))
        self.this_year[loser] += self.k * (0 - (1 / (1 + 10 ** ((self.this_year[loser] - self.this_year[winner]) / 400))))
        if self.this_year[winner] < 0:
            self.this_year[winner] = 0
        if self.this_year[loser] < 0:
            self.this_year[loser] = 0

    def update_elo_last_3(self, winner, loser):
        self.last_3[winner] += self.k * (1 - (1 / (1 + 10 ** ((self.last_3[winner] - self.last_3[loser]) / 400))))
        self.last_3[loser] += self.k * (0 - (1 / (1 + 10 ** ((self.last_3[loser] - self.last_3[winner]) / 400))))
        if self.last_3[winner] < 0:
            self.last_3[winner] = 0
        if self.last_3[loser] < 0:
            self.last_3[loser] = 0

    def get_elo(self):
        for year in range(2000, 2026):
            with open(f"year_stats/{year}", 'r') as file:
                elo_f = file.read()

            for line in elo_f.split("\n"):
                game = line.split(',')
                if len(game) > 10 and "Winner" not in game:
                    winner = game[10]
                    loser = game[11]
                    self.update_elo(winner, loser)
    
    # Gets the elo rating of players over the last 3 years
    def last_3_years(self, years):

        for year in range(years - 3, years):
            with open(f"year_stats/{year}", 'r') as file:
                elo_f = file.read()

            for line in elo_f.split("\n"):
                game = line.split(',')
                if len(game) > 10 and "Winner" not in game:
                    winner = game[10]
                    self.last_3[winner] = 1500
                    loser = game[11]
                    self.last_3[loser] = 1500

        for year in range(years - 3, years):
            with open(f"year_stats/{year}", 'r') as file:
                elo_f = file.read()

            for line in elo_f.split("\n"):
                game = line.split(',')
                if len(game) > 10 and "Winner" not in game:
                    winner = game[10]
                    loser = game[11]
                    self.update_elo_last_3(winner, loser)

    # Gets the elo rating of players over the current year
    def this_year_elo(self, year):
        with open(f"year_stats/{year}", 'r') as file:
                elo_f = file.read()

        for line in elo_f.split("\n"):
            game = line.split(',')
            if len(game) > 10 and "Winner" not in game:
                winner = game[10]
                if winner not in self.last_3:
                    self.this_year[winner] = 1500
                else:
                    self.this_year[winner] = (11 * 1500 + 1 * self.last_3[winner]) / 12
                loser = game[11]
                if loser not in self.last_3:
                    self.this_year[loser] = 1500
                else:
                    self.this_year[loser] = (11 * 1500 + 1 * self.last_3[loser]) / 12

        for line in elo_f.split("\n"):
            game = line.split(',')
            if len(game) > 10 and "Winner" not in game:
                winner = game[10]
                loser = game[11]
                self.update_elo_this_year(winner, loser, year)


def main():
    tennis = Elo()

    year = int(input("Enter year: "))
    tennis.populate_elo()
    tennis.get_elo()
    tennis.last_3_years(year)
    #names.to_string()
    tennis.this_year_elo(year)
    tennis.year_to_string()

if __name__ == "__main__":
    main()