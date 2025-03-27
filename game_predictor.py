import elo_rating as e

player1 = input("Enter player 1: ")
player2 = input("Enter player 2: ")
surface = input("Enter surface: ")

elo = e.Elo()
elo.last_3_years(2025)
elo.this_year_elo(2025)
elo.get_surface_elo(2025, surface)

elo1 = elo.surface_elo[player1]
elo2 = elo.surface_elo[player2]

print(f"{player1} has an elo rating of {elo1} on a {surface.lower()} surface")
print(f"{player2} has an elo rating of {elo2} on a {surface.lower()} surface")

player_win_chance = 1 / (1 + 10 ** ((elo2 - elo1) / 400))

print(f"{player1} has a {player_win_chance:.2%} chance of beating {player2}")