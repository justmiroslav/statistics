import matplotlib.pyplot as plt
import seaborn as sns
from calculations import battle_data

winner_elixir_levels = []
loser_elixir_levels = []
total_damage_list = []

for battle in battle_data:
    winner_elixir = float(battle["winnerElixir"])
    loser_elixir = float(battle["loserElixir"])
    total_damage = float(battle["totalDamage"])

    winner_elixir_levels.append(winner_elixir)
    loser_elixir_levels.append(loser_elixir)
    total_damage_list.append(total_damage)

plt.figure(figsize=(12, 6))
plt.hist(winner_elixir_levels, bins=20, alpha=0.5, label='Winner Elixir Levels', color='green')
plt.hist(loser_elixir_levels, bins=20, alpha=0.5, label='Loser Elixir Levels', color='orange')
plt.xlabel('Elixir Levels')
plt.ylabel('Frequency')
plt.legend()
plt.title('Distribution of Elixir Levels for Winners and Losers')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(total_damage_list, bins=20, kde=True, color='purple')
plt.xlabel('Total Damage')
plt.ylabel('Frequency')
plt.title('Distribution of Total Damage')
plt.show()

similar_elixir_damage = []
dissimilar_elixir_damage = []

for battle in battle_data:
    winner_elixir = float(battle["winnerElixir"])
    loser_elixir = float(battle["loserElixir"])
    total_damage = float(battle["totalDamage"])

    elixir_threshold = 0.2

    # Check if elixir levels are similar
    if abs(winner_elixir - loser_elixir) <= elixir_threshold:
        similar_elixir_damage.append(total_damage)
    else:
        dissimilar_elixir_damage.append(total_damage)

plt.figure(figsize=(10, 6))
plt.hist(similar_elixir_damage, bins=20, alpha=0.5, label='Similar Elixir Levels', color='blue')
plt.hist(dissimilar_elixir_damage, bins=20, alpha=0.5, label='Dissimilar Elixir Levels', color='red')
plt.xlabel('Total Damage')
plt.ylabel('Frequency')
plt.legend()
plt.title('Distribution of Total Damage based on Elixir Levels')
plt.show()

# Analyze the likelihood of total damage over 12000 based on elixir levels
total_similar_elixir_matches = len(similar_elixir_damage)
total_dissimilar_elixir_matches = len(dissimilar_elixir_damage)

similar_elixir_high_damage = sum(1 for damage in similar_elixir_damage if damage > 12000)
dissimilar_elixir_high_damage = sum(1 for damage in dissimilar_elixir_damage if damage > 12000)

percentage_similar_elixir_high_damage = (similar_elixir_high_damage / total_similar_elixir_matches) * 100
percentage_dissimilar_elixir_high_damage = (dissimilar_elixir_high_damage / total_dissimilar_elixir_matches) * 100

labels = ['Similar Elixir Levels', 'Dissimilar Elixir Levels']
percentages = [percentage_similar_elixir_high_damage, percentage_dissimilar_elixir_high_damage]

plt.figure(figsize=(8, 5))
plt.bar(labels, percentages, color=['blue', 'red'])
plt.ylim(0, 100)
plt.ylabel('Percentage of Matches with Total Damage > 12000')
plt.title('Likelihood of Total Damage > 12000 based on Elixir Levels')
plt.show()

# Visualize the correlation between elixir levels and total damage
high_damage_matches = [battle for battle in battle_data if int(battle["totalDamage"]) > 12000]
winnerElixir = [float(elx["winnerElixir"]) for elx in high_damage_matches]
loserElixir = [float(elx["loserElixir"]) for elx in high_damage_matches]

plt.figure(figsize=(10, 6))
plt.scatter(winnerElixir, loserElixir, label='Winner vs. Loser Elixir')
plt.axline([0, 0], slope=1, color='red', linestyle='--', label='Equal Elixir Line')
plt.title('Elixir Levels in Matches with Total Damage over 12000')
plt.xlabel('Winner Elixir')
plt.ylabel('Loser Elixir')
plt.legend()
plt.show()
