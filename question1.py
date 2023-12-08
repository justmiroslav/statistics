import csv
import matplotlib.pyplot as plt

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

combinations = []
winner_deck_rarity_count = {}
loser_deck_rarity_count = {}
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

for battle in battle_data[:100000]:
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
plt.pie(winner_percentages, labels=labels, autopct="%1.1f%%", colors=["green", "lightgrey", "brown", "purple"])
plt.title("Winner Deck Card Rarity")
plt.show()

labels = list(loser_deck_rarity_count.keys())
plt.pie(loser_percentages, labels=labels, autopct="%1.1f%%", colors=["blue", "yellow", "red", "pink"])
plt.title("Loser Deck Card Rarity")
plt.show()

for rarity in rarity_win_loss:
    totals = rarity_win_loss[rarity]["winners"] + rarity_win_loss[rarity]["losers"]
    winner_pct = rarity_win_loss[rarity]["winners"] / totals * 100
    loser_pct = rarity_win_loss[rarity]["losers"] / totals * 100
    labels = ["Winners", "Losers"]
    values = [winner_pct, loser_pct]
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title(f"{rarity} Rarity Win/Loss Percentage")
    plt.show()

for rarity in battles_by_rarity:
    counts = list(battles_by_rarity[rarity].keys())
    counts.sort(key=int)
    values = []
    labels = []
    for count in counts:
        total_battles = (battles_by_rarity[rarity][count]["winner"] +
                         battles_by_rarity[rarity][count]["loser"])
        wins = battles_by_rarity[rarity][count]["winner"]
        win_rate = wins / total_battles * 100
        rarity_win_rates[rarity][count] = win_rate
        values.append(win_rate)
        labels.append(str(count))
    plt.bar(labels, values)
    for i, v in enumerate(values):
        plt.text(i, v + 0.5, str(round(v, 1)) + "%", ha="center")
    plt.xlabel("Number of Cards")
    plt.ylabel("Win Rate, %")
    plt.title(f"Win Rate by Number of {rarity} cards")
    plt.show()

for l in rarity_win_rates["Legendary"]:
    for e in rarity_win_rates["Epic"]:
        for r in rarity_win_rates["Rare"]:
            for c in rarity_win_rates["Common"]:
                if l + e + r + c != 8:
                    continue
                total_win_rate = (rarity_win_rates["Legendary"][l] +
                                  rarity_win_rates["Epic"][e] +
                                  rarity_win_rates["Rare"][r] +
                                  rarity_win_rates["Common"][c]) / 4
                combinations.append([[l, e, r, c], total_win_rate])

combinations.sort(key=lambda x: x[1], reverse=True)
best_combinations = combinations[:3]

labels_list = ["Legendary", "Epic", "Rare", "Common"]
colors = ["gold", "lightskyblue", "lightcoral", "lightgreen"]

for i, (combination, win_rate) in enumerate(best_combinations):
    plt.figure()
    plt.bar(labels_list, combination, color=colors)
    plt.xlabel("Card Rarity")
    plt.ylabel("Number of Cards")
    plt.title(f"Top {i + 1} Combination\nWin Rate: {round(win_rate, 2)}%")
    plt.show()
