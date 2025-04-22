import elo_rating as e

player1 = input("Enter player 1: ")
player2 = input("Enter player 2: ")
surface = input("Enter surface: ")

elo = e.Elo()
elo.last_3_years(2025)
elo.this_year_elo(2025)
elo.get_surface_elo(2025, surface)
'''
selo1 = elo.surface_elo[player1]
selo2 = elo.surface_elo[player2]
'''
elo1 = elo.this_year[player1]
elo2 = elo.this_year[player2]

# print(f"{player1} has a surface elo rating of {selo1} on a {surface.lower()} surface")
# print(f"{player2} has a surface elo rating of {selo2} on a {surface.lower()} surface")

print(f"{player1} has an overall elo rating of {elo1}")
print(f"{player2} has an overall elo rating of {elo2}")

player_win_chance = 1 / (1 + 10 ** ((elo2 - elo1) / 400))

print(f"{player1} has a {player_win_chance:.2%} chance of beating {player2}")
'''
s_player_win_chance = 1 / (1 + 10 ** ((selo2 - selo1) / 400))
print(f"{player1} has a {s_player_win_chance:.2%} chance of beating {player2} on a {surface.lower()} surface")
'''
