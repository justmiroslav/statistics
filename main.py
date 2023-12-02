import csv
from collections import defaultdict
import statistics
import matplotlib.pyplot as plt
import pandas as pd
import ast

card_data = pd.read_csv('statistics/CartIdName.csv')

# Extract card IDs from deck strings
def extract_card_ids(deck_str):
    try:
        deck = ast.literal_eval(deck_str)
        return [card[0] for card in deck]
    except (ValueError, SyntaxError):
        return []

# Process battle data
def process_battle_data():
    num_battles = 0
    battle_stats = defaultdict(list)
    card_usage = defaultdict(lambda: defaultdict(int))
    card_damage = defaultdict(lambda: defaultdict(int))
    card_trophies = defaultdict(lambda: defaultdict(int))

    with open("statistics/ClashRoyaleData.csv") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header

        for row in reader:
            if num_battles >= 10000:
                break
            winner_trophies_start, loser_trophies_start = int(row[4]), int(row[5])
            winner_trophies_end, loser_trophies_end = int(row[6]), int(row[7])
            winner_damage, loser_damage = int(row[12]), int(row[13])
            winner_diff, loser_diff = winner_trophies_end - winner_trophies_start, loser_trophies_start - loser_trophies_end

            battle_stats["winner"].append(winner_diff)
            battle_stats["loser"].append(loser_diff)

            winner_deck, loser_deck = extract_card_ids(row[8]), extract_card_ids(row[9])
            for card in winner_deck:
                card_usage[card]['winner'] += 1
                card_damage[card]['winner'] += winner_damage
                card_trophies[card]['winner'] += winner_diff
            for card in loser_deck:
                card_usage[card]['loser'] += 1
                card_damage[card]['loser'] += loser_damage
                card_trophies[card]['loser'] += loser_diff

            num_battles += 1

    return battle_stats, card_usage, card_trophies, card_damage

    avg_winner_diff = sum(battle_stats["winner"]) / len(battle_stats["winner"])
    max_winner_diff = max(battle_stats["winner"])
    min_winner_diff = min(battle_stats["winner"])
    std_winner_diff = statistics.stdev(battle_stats["winner"])

    avg_loser_diff = sum(battle_stats["loser"]) / len(battle_stats["loser"])
    max_loser_diff = max(battle_stats["loser"])
    min_loser_diff = min(battle_stats["loser"])
    std_loser_diff = statistics.stdev(battle_stats["loser"])

    # Converting card usage, damage, and trophies data to DataFrames
    card_usage_df = pd.DataFrame(card_usage).T
    card_damage_df = pd.DataFrame(card_damage).T
    card_trophies_df = pd.DataFrame(card_trophies).T
    card_usage_df = card_usage_df.merge(card_data, left_index=True, right_on='team.card1.id')
    card_damage_df = card_damage_df.merge(card_data, left_index=True, right_on='team.card1.id')
    card_trophies_df = card_trophies_df.merge(card_data, left_index=True, right_on='team.card1.id')

    return (
        avg_winner_diff, max_winner_diff, min_winner_diff, std_winner_diff,
        avg_loser_diff, max_loser_diff, min_loser_diff, std_loser_diff,
        card_usage_df, card_trophies_df, card_damage_df,
    )

# Plotting graphs
def plot_graphs(avg_winner_diff, avg_loser_diff, max_winner_diff, max_loser_diff, min_winner_diff, min_loser_diff,
                std_winner_diff, std_loser_diff, card_usage_df, card_trophies_df, card_damage_df):
    # Average trophy change
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    plt.bar(['Winners', 'Losers'], [avg_winner_diff, avg_loser_diff], color=['blue', 'red'])
    plt.title('Average Trophy Change')
    plt.ylabel('Trophies')

    # Maximum and minimum trophy change
    plt.subplot(2, 2, 2)
    plt.bar(['Max Winner', 'Max Loser'], [max_winner_diff, max_loser_diff], color=['green', 'orange'])
    plt.bar(['Min Winner', 'Min Loser'], [min_winner_diff, min_loser_diff], color=['purple', 'brown'])
    plt.title('Max and Min Trophy Change')
    plt.ylabel('Trophies')

    # Trophy change variability
    plt.subplot(2, 2, 3)
    plt.bar(['Winners', 'Losers'], [std_winner_diff, std_loser_diff], color=['cyan', 'magenta'])
    plt.title('Trophy Change Variability (Standard Deviation)')
    plt.ylabel('Trophies')

    # Frequency of trophy changes
    plt.subplot(2, 2, 4)
    plt.hist(battle_stats["winner"], bins=20, alpha=0.5, label='Winners')
    plt.hist(battle_stats["loser"], bins=20, alpha=0.5, label='Losers')
    plt.xlabel('Trophy Change')
    plt.ylabel('Frequency')
    plt.title('Distribution of Trophy Changes')
    plt.legend()

    plt.tight_layout()

    # Card frequency in winning vs. losing decks
    plt.figure(figsize=(12, 6))
    ax = card_usage_df.sort_values('winner', ascending=False).head(10).plot(x='team.card1.name', y=['winner', 'loser'], kind='bar', stacked=False)
    plt.title('Top 10 Cards in Winning and Losing Decks')
    plt.ylabel('Usage Frequency')
    plt.xlabel('Card Name')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels and adjust their alignment
    plt.tight_layout()  # Ensures everything fits in the plot area

    # Card impact on trophy gains
    plt.figure(figsize=(12, 6))
    card_trophies_df['avg_trophy_gain'] = card_trophies_df['winner'] / card_usage_df['winner']
    card_trophies_df.sort_values('avg_trophy_gain', ascending=False).head(10).plot(x='team.card1.name', y='avg_trophy_gain', kind='bar', color='green')
    plt.title('Average Trophy Gain for Top 10 Cards')
    plt.ylabel('Average Trophy Gain')
    plt.xlabel('Card Name')

    # Card impact on damage dealt
    plt.figure(figsize=(14, 6))
    card_damage_df['avg_damage'] = card_damage_df['winner'] / card_usage_df['winner']
    card_damage_df.sort_values('avg_damage', ascending=False).head(10).plot(x='team.card1.name', y='avg_damage', kind='bar', color='orange')
    plt.title('Average Damage Dealt for Top 10 Cards')
    plt.ylabel('Average Damage')
    plt.xlabel('Card Name')

    # Average damage difference for top 10 most frequently used cards
    card_damage_diff = defaultdict(list)

    for index, row in pd.read_csv("statistics/ClashRoyaleData.csv").iterrows():
        winner_deck = extract_card_ids(row[8])
        loser_deck = extract_card_ids(row[9])
        damage_diff = int(row[12]) - int(row[13])
        for card in winner_deck:
            card_damage_diff[card].append(damage_diff)
        for card in loser_deck:
            card_damage_diff[card].append(-damage_diff)

    avg_card_damage_diff = {card: sum(diffs) / len(diffs) for card, diffs in card_damage_diff.items() if diffs}

    avg_card_damage_diff_df = pd.DataFrame(list(avg_card_damage_diff.items()), columns=['CardID', 'AvgDamageDiff'])
    avg_card_damage_diff_df = avg_card_damage_diff_df.merge(card_data, left_on='CardID', right_on='team.card1.id')

    top_cards_damage_diff = avg_card_damage_diff_df.sort_values(by='AvgDamageDiff', ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    plt.bar(top_cards_damage_diff['team.card1.name'], top_cards_damage_diff['AvgDamageDiff'], color='purple')
    plt.title('Average Damage Difference for Top 10 Most Frequently Used Cards')
    plt.xlabel('Card Name')
    plt.ylabel('Average Damage Difference')
    plt.xticks(rotation=45)

    plt.show()

if __name__ == "__main__":
    battle_stats, card_usage, card_trophies, card_damage = process_battle_data()
