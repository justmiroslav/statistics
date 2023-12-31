import csv
import matplotlib.pyplot as plt

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

combinations = []
winner_deck_rarity_count = {}
loser_deck_rarity_count = {}
labels_list = ["Legendary", "Epic", "Rare", "Common"]
colors = ["gold", "lightskyblue", "lightcoral", "lightgreen"]
rarity_win_loss = {
    "Common": {"winners": 0, "losers": 0},
    "Rare": {"winners": 0, "losers": 0},
    "Epic": {"winners": 0, "losers": 0},
    "Legendary": {"winners": 0, "losers": 0}
}
battles_by_rarity = {
    "Common": {},
    "Rare": {},
    "Epic": {},
    "Legendary": {}
}
rarity_win_rates = {
    "Common": {},
    "Rare": {},
    "Epic": {},
    "Legendary": {}
}

def get_card_rarity(card_id):
    for element in card_data:
        if element["п»їCardId"] == str(card_id):
            return element["CardRarity"]

def count_rarity(deck, this_rarity):
    counter = 0
    for element in deck:
        if get_card_rarity(element[0]) == this_rarity:
            counter += 1
    return counter

for battle in battle_data:
    winner_deck = eval(battle["winnerDeck"])
    loser_deck = eval(battle["loserDeck"])

    for rarity in battles_by_rarity:
        winner_count = count_rarity(winner_deck, rarity)
        loser_count = count_rarity(loser_deck, rarity)
        if winner_count not in battles_by_rarity[rarity]:
            battles_by_rarity[rarity][winner_count] = {"winner": 0, "loser": 0}
        if loser_count not in battles_by_rarity[rarity]:
            battles_by_rarity[rarity][loser_count] = {"winner": 0, "loser": 0}
        battles_by_rarity[rarity][winner_count]["winner"] += 1
        battles_by_rarity[rarity][loser_count]["loser"] += 1

    for card in winner_deck:
        rarity = get_card_rarity(card[0])
        winner_deck_rarity_count[rarity] = winner_deck_rarity_count.get(rarity, 0) + 1
        rarity_win_loss[rarity]["winners"] += 1

    for card in loser_deck:
        rarity = get_card_rarity(card[0])
        loser_deck_rarity_count[rarity] = loser_deck_rarity_count.get(rarity, 0) + 1
        rarity_win_loss[rarity]["losers"] += 1

total_winner = sum(winner_deck_rarity_count.values())
winner_percentages = [(v/total_winner)*100 for v in winner_deck_rarity_count.values()]

total_loser = sum(loser_deck_rarity_count.values())
loser_percentages = [(v/total_loser)*100 for v in loser_deck_rarity_count.values()]

labels = list(winner_deck_rarity_count.keys())
plt.pie(winner_percentages, labels=labels, autopct="%1.2f%%", colors=["green", "lightgrey", "brown", "purple"])
plt.title("Winner deck rarity distribution")
plt.show()

labels = list(loser_deck_rarity_count.keys())
plt.pie(loser_percentages, labels=labels, autopct="%1.2f%%", colors=["blue", "yellow", "red", "pink"])
plt.title("Loser deck rarity distribution")
plt.show()

for rarity in rarity_win_loss:
    totals = rarity_win_loss[rarity]["winners"] + rarity_win_loss[rarity]["losers"]
    winner_pct = rarity_win_loss[rarity]["winners"] / totals * 100
    loser_pct = rarity_win_loss[rarity]["losers"] / totals * 100
    labels = ["Winners", "Losers"]
    values = [winner_pct, loser_pct]
    plt.pie(values, labels=labels, autopct="%1.2f%%")
    plt.title(f"{rarity} rarity Win/Loss chances")
    plt.show()

for rarity in battles_by_rarity:
    counts = list(battles_by_rarity[rarity].keys())
    battles = sum([sum(battles_by_rarity[rarity][c].values()) for c in counts])
    counts.sort(key=int)
    values = []
    labels = []
    percentages = []
    for count in counts:
        rarity_win_rates[rarity][count] = {"win_rate": 0, "kf": 0}
        count_battles = sum(battles_by_rarity[rarity][count].values())
        total_battles = (battles_by_rarity[rarity][count]["winner"] +
                         battles_by_rarity[rarity][count]["loser"])
        wins = battles_by_rarity[rarity][count]["winner"]
        win_rate = wins / total_battles * 100
        percentage = count_battles / battles * 100
        rarity_win_rates[rarity][count]["win_rate"] = win_rate
        rarity_win_rates[rarity][count]["kf"] = win_rate * percentage
        values.append(win_rate)
        percentages.append(percentage)
        labels.append(str(count))
    plt.bar(labels, values)
    for i, v in enumerate(values):
        plt.text(i, v + 0.5, str(round(v, 2)) + "%", ha="center")
    plt.xlabel("Number of Cards")
    plt.ylabel("Win Rate, %")
    plt.title(f"Win rate for numbers of {rarity} rarity cards")
    plt.show()
    plt.bar(labels, percentages)
    for i, v in enumerate(percentages):
        plt.text(i, v + 0.5, str(round(v, 2)) + "%", ha="center")
    plt.xlabel("Number of Cards")
    plt.ylabel("Percentage of Battles, %")
    plt.title(f"% Battles for numbers of {rarity} rarity cards")
    plt.show()

for l, d in rarity_win_rates["Legendary"].items():
    for e, a in rarity_win_rates["Epic"].items():
        for r, s in rarity_win_rates["Rare"].items():
            for c, w in rarity_win_rates["Common"].items():
                if l + e + r + c != 8:
                    continue
                total_win_rate = (d["win_rate"] + a["win_rate"] + s["win_rate"] + w["win_rate"]) / 4
                total_kf = (d["kf"] + a["kf"] + s["kf"] + w["kf"])
                combination = [l, e, r, c]
                combinations.append([combination, total_win_rate, total_kf])

combinations.sort(key=lambda x: x[2], reverse=True)
combinations = combinations[:3]

best_combinations = sorted(combinations, key=lambda x: x[1], reverse=True)
print(f"best_combinations - {best_combinations}")
for i, (combination, win_rate, kf) in enumerate(best_combinations):
    plt.figure()
    plt.bar(labels_list, combination, color=colors)
    plt.xlabel("Card Rarity")
    plt.ylabel("Number of Cards")
    plt.title(f"Top {i + 1} Combination\nWin Rate: {round(win_rate, 2)}%")
    plt.show()
