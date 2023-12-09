import csv
import matplotlib.pyplot as plt
import seaborn as sns

battle_data = []
card_data = []

with open("BattleData.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        battle_data.append(row)

with open("CardData.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        card_data.append(row)

print(f"Total battles: {len(battle_data)}")

card_popularity = {}
total_matches_with_high_damage = []
total_winner_damage = []
total_loser_damage = []
elx_winner = {}
elx_loser = {}
elx_winner_avg = {}
elx_loser_avg = {}

def get_card_rarity(this_card_id):
    for card in card_data:
        if card["ï»¿CardId"] == str(this_card_id):
            return card["CardRarity"]

def count_rarity(deck, rarity):
    counter = 0
    for card in deck:
        if get_card_rarity(card[0]) == rarity:
            counter += 1
    return counter

def get_card_name(card_id):
    for card in card_data:
        if card["ï»¿CardId"] == str(card_id):
            return card["CardName"]

for battle in battle_data:
    winner_deck = eval(battle["winnerDeck"])
    loser_deck = eval(battle["loserDeck"])
    total_winner_damage.append(int(battle["winnerDamage"]))
    total_loser_damage.append(int(battle["loserDamage"]))

    # Count the popularity of each card
    for card_id, _ in winner_deck:
        card_name = get_card_name(card_id)
        card_popularity[card_name] = card_popularity.get(card_name, 0) + 1

    for card_id, _ in loser_deck:
        card_name = get_card_name(card_id)
        card_popularity[card_name] = card_popularity.get(card_name, 0) + 1

    if int(battle["totalDamage"]) > 12000:
        total_matches_with_high_damage.append(1)

    elx_winner.setdefault(float(battle["winnerElixir"]), []).append(int(battle["winnerDamage"]))
    elx_loser.setdefault(float(battle["loserElixir"]), []).append(int(battle["loserDamage"]))

for elixir_avg, damages in elx_winner.items():
    elx_winner_avg[round(elixir_avg, 3)] = round(sum(damages) / len(damages), 3)

for elixir_avg, damages in elx_loser.items():
    elx_loser_avg[round(elixir_avg, 3)] = round(sum(damages) / len(damages), 3)

avg_winner_damage = sum(total_winner_damage) / len(total_winner_damage)
avg_loser_damage = sum(total_loser_damage) / len(total_loser_damage)

# Get the top 10 most popular cards
top_10_cards = sorted(card_popularity.items(), key=lambda x: x[1], reverse=True)[:10]
top_10_card_names = [card[0] for card in top_10_cards]
top_10_card_counts = [card[1] for card in top_10_cards]

# Visualize the top 10 most popular cards
plt.figure(figsize=(10, 6))
sns.barplot(x=top_10_card_counts, y=top_10_card_names, palette="viridis")
plt.title("Top 10 Most Popular Cards")
plt.xlabel("Number of Appearances")
plt.ylabel("Card Name")
plt.show()

categories = ["Average Winner Damage", "Average Loser Damage"]
values = [avg_winner_damage, avg_loser_damage]

plt.figure(figsize=(8, 5))
sns.barplot(x=categories, y=values, palette="coolwarm")
plt.title("Average Damage Comparison")
plt.ylabel("Average Damage")
plt.show()

del elx_winner_avg[4.75]  # deleted probably incorrect data as avg damage for elixir level 4.75 is 0
win_elixir_levels = [round(elx_level) for elx_level in elx_winner_avg.keys()]
win_avg_damage_per_level = [damage for damage in elx_winner_avg.values()]
plt.figure(figsize=(8, 5))
sns.barplot(x=win_elixir_levels, y=win_avg_damage_per_level, palette="crest")
plt.title("Average Damage For Each Elixir Level For Winners")
plt.xlabel("Elixir Level")
plt.ylabel("Average Damage")
plt.show()

lose_elixir_levels = [round(elx_level) for elx_level in elx_loser_avg.keys()]
lose_avg_damage_per_level = [damage for damage in elx_loser_avg.values()]
plt.figure(figsize=(8, 5))
sns.barplot(x=lose_elixir_levels, y=lose_avg_damage_per_level, palette="rocket")
plt.title("Average Damage For Each Elixir Level For Losers")
plt.xlabel("Elixir Level")
plt.ylabel("Average Damage")
plt.show()

percentage_of_matches_with_high_damage = (sum(total_matches_with_high_damage) / len(battle_data)) * 100
labels = ["Matches with High Damage", "Matches with Low Damage"]
sizes = [percentage_of_matches_with_high_damage, 100 - percentage_of_matches_with_high_damage]
colors = ["lightcoral", "lightskyblue"]
plt.figure(figsize=(8, 5))
plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
plt.title("Percentage of Matches with Total Damage over 12000")
plt.show()
