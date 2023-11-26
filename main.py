import csv
from collections import defaultdict

num_battles = 0
battle_stats = defaultdict(list)

with open("ClashRoyaleData.csv") as f:
    reader = csv.reader(f)
    next(reader)

    for row in reader:
        if num_battles >= 10000:
            break
        winner_trophies_start = int(row[4])
        loser_trophies_start = int(row[5])
        winner_trophies_end = int(row[6])
        loser_trophies_end = int(row[7])

        winner_diff = winner_trophies_end - winner_trophies_start
        loser_diff = loser_trophies_start - loser_trophies_end

        battle_stats["winner"].append(winner_diff)
        battle_stats["loser"].append(loser_diff)

        num_battles += 1

avg_winner_diff = sum(battle_stats["winner"]) / len(battle_stats["winner"])
max_winner_diff = max(battle_stats["winner"])
min_winner_diff = min(battle_stats["winner"])

avg_loser_diff = sum(battle_stats["loser"]) / len(battle_stats["loser"])
max_loser_diff = max(battle_stats["loser"])
min_loser_diff = min(battle_stats["loser"])

print(f"Average winner trophy change: {avg_winner_diff:.2f}")
print(f"Maximum winner trophy change: {max_winner_diff}")
print(f"Minimum winner trophy change: {min_winner_diff}")

print(f"Average loser trophy change: {avg_loser_diff:.2f}")
print(f"Maximum loser trophy change: {max_loser_diff}")
print(f"Minimum loser trophy change: {min_loser_diff}")
