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

for battle in battle_data[:1000]:
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

print(f"1 - Total battles: {len(battle_data)}")
print(f"2.1 - Top 10 win cards: {win_cards_names}")
print(f"2.2 - Top 10 lose cards: {lose_cards_names}")
print(f"3.1 - Average winner damage: {sum(total_winner_damage)/len(total_winner_damage):.2f}")
print(f"3.2 - Average loser damage: {sum(total_loser_damage)/len(total_loser_damage):.2f}")
print(f"4.1 - Average damage for each elixir level for winners: {elx_winner_avg}")
print(f"4.2 - Average damage for each elixir level for losers: {elx_loser_avg}")
print(f"5 - Percentage of matches with total damage over 12000: {(sum(total_matches_with_high_damage)/1000)*100:.2f}%")

card_names = [details[0] for details in win_cards_names.values()]
win_counts = [details[3] for details in win_cards_names.values()]
lose_card_names = [details[0] for details in lose_cards_names.values()]
lose_counts = [details[3] for details in lose_cards_names.values()]
avg_winner_damage = sum(total_winner_damage) / len(total_winner_damage)
avg_loser_damage = sum(total_loser_damage) / len(total_loser_damage)

plt.figure(figsize=(10, 6))
sns.barplot(x=card_names, y=win_counts, palette="viridis")
plt.title("Top 10 Win Cards in Clash Royale")
plt.xlabel("Card Name")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x=lose_card_names, y=lose_counts, palette="magma")
plt.title("Top 10 Lose Cards in Clash Royale")
plt.xlabel("Card Name")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()

categories = ['Average Winner Damage', 'Average Loser Damage']
values = [avg_winner_damage, avg_loser_damage]

plt.figure(figsize=(8, 5))
sns.barplot(x=categories, y=values, palette="coolwarm")
plt.title("Average Damage Comparison")
plt.ylabel("Average Damage")
plt.show()
