import csv
import matplotlib.pyplot as plt
import seaborn as sns

battle_data = []
card_data = []

with open("ClashRoyaleData.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        battle_data.append(row)

with open("IdNameRarityCost.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        card_data.append(row)

print(f"Total battles: {len(battle_data)}")
win_cards = {}
lose_cards = {}
win_cards_names = {}
lose_cards_names = {}
total_matches_with_high_damage = []
total_winner_damage = []
total_loser_damage = []
elx_winner = {}
elx_loser = {}
elx_winner_avg = {}
elx_loser_avg = {}

def get_card_rarity(this_card_id):
    for card in card_data:
        if card["п»їCardId"] == str(this_card_id):
            return card["CardRarity"]

def count_rarity(deck, rarity):
    counter = 0
    for card in deck:
        if get_card_rarity(card[0]) == rarity:
            counter += 1
    return counter

for battle in battle_data[:100000]:
    winner_deck = eval(battle["winnerDeck"])
    loser_deck = eval(battle["loserDeck"])
    total_winner_damage.append(int(battle["winnerDamage"]))
    total_loser_damage.append(int(battle["loserDamage"]))

    if int(battle["totalDamage"]) > 12000:
        total_matches_with_high_damage.append(1)

    elx_winner.setdefault(float(battle["winnerElixir"]), []).append(int(battle["winnerDamage"]))
    elx_loser.setdefault(float(battle["loserElixir"]), []).append(int(battle["loserDamage"]))

    for card_id, level in winner_deck:
        win_cards[str(card_id)] = win_cards.get(str(card_id), 0) + 1

    for card_id, level in loser_deck:
        lose_cards[str(card_id)] = lose_cards.get(str(card_id), 0) + 1

win_cards_list = sorted(win_cards.items(), key=lambda y: y[1], reverse=True)[:10]
lose_cards_list = sorted(lose_cards.items(), key=lambda y: y[1], reverse=True)[:10]

for card_id, count in win_cards_list:
    for x in card_data:
        if str(card_id) == x["п»їCardId"]:
            win_cards_names[card_id] = [x["CardName"], x["CardRarity"], x["CardCost"], count]

for card_id, count in lose_cards_list:
    for x in card_data:
        if str(card_id) == x["п»їCardId"]:
            lose_cards_names[card_id] = [x["CardName"], x["CardRarity"], x["CardCost"], count]

for elixir_avg, damages in elx_winner.items():
    elx_winner_avg[round(elixir_avg, 3)] = round(sum(damages) / len(damages), 3)

for elixir_avg, damages in elx_loser.items():
    elx_loser_avg[round(elixir_avg, 3)] = round(sum(damages) / len(damages), 3)

card_names = [details[0] for details in win_cards_names.values()]
win_counts = [details[3] for details in win_cards_names.values()]
lose_card_names = [details[0] for details in lose_cards_names.values()]
lose_counts = [details[3] for details in lose_cards_names.values()]
avg_winner_damage = sum(total_winner_damage) / len(total_winner_damage)
avg_loser_damage = sum(total_loser_damage) / len(total_loser_damage)

win_counts_sum = sum(win_counts)
win_percentage = [count / win_counts_sum * 100 for count in win_counts]

plt.figure(figsize=(8, 8))
plt.pie(win_percentage, labels=card_names, autopct="%1.1f%%", startangle=140)
plt.title("Top 10 Win Cards")
plt.show()

lose_counts_sum = sum(lose_counts)
lose_percentage = [count / lose_counts_sum * 100 for count in lose_counts]

plt.figure(figsize=(8, 8))
plt.pie(lose_percentage, labels=lose_card_names, autopct="%1.1f%%", startangle=140)
plt.title("Top 10 Lose Cards")
plt.show()

categories = ["Average Winner Damage", "Average Loser Damage"]
values = [avg_winner_damage, avg_loser_damage]

plt.figure(figsize=(8, 5))
sns.barplot(x=categories, y=values, palette="coolwarm")
plt.title("Average Damage Comparison")
plt.ylabel("Average Damage")
plt.show()

del elx_winner_avg[4.75]  # deleted probably incorrect data as avg damage for elixir level 4.75 is 0
win_elixir_levels = [round(elx_level, 1) for elx_level in elx_winner_avg.keys()]
win_avg_damage_per_level = [damage for damage in elx_winner_avg.values()]
plt.figure(figsize=(12, 5))
sns.barplot(x=win_elixir_levels, y=win_avg_damage_per_level, palette="crest")
plt.title("Average Damage For Each Elixir Level For Winners")
plt.xlabel("Elixir Level")
plt.ylabel("Average Damage")
plt.show()

lose_elixir_levels = [round(elx_level, 1) for elx_level in elx_loser_avg.keys()]
lose_avg_damage_per_level = [damage for damage in elx_loser_avg.values()]
plt.figure(figsize=(12, 5))
sns.barplot(x=lose_elixir_levels, y=lose_avg_damage_per_level, palette="rocket")
plt.title("Average Damage For Each Elixir Level For Losers")
plt.xlabel("Elixir Level")
plt.ylabel("Average Damage")
plt.show()

percentage_of_matches_with_high_damage = (sum(total_matches_with_high_damage) / 1000) * 100
labels = ["Matches with High Damage", "Matches with Low Damage"]
sizes = [percentage_of_matches_with_high_damage, 100 - percentage_of_matches_with_high_damage]
colors = ["lightcoral", "lightskyblue"]
plt.figure(figsize=(8, 5))
plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
plt.title("Percentage of Matches with Total Damage over 12000")
plt.show()
