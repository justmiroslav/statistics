import csv
import matplotlib.pyplot as plt

battle_data = []
with open("BattleData.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        battle_data.append(row)

elixir_level_differences = []

for battle in battle_data:
    if int(battle["totalDamage"]) > 12000:
        winner_elixir = float(battle["winnerElixir"])
        loser_elixir = float(battle["loserElixir"])
        diff = abs(winner_elixir - loser_elixir)
        elixir_level_differences.append(diff)

bin_edges = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
             1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

plt.figure(figsize=(10, 6))
plt.hist(elixir_level_differences, bins=bin_edges, color="skyblue", edgecolor="black")
plt.title("Elixir Level Differences in High-Damage Battles")
plt.xlabel("Elixir Level Difference")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()
