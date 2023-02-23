import random

# Create a deck of cards
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4

# Define a function to calculate the value of a hand
def calculate_hand(hand):
    value = 0
    aces = 0
    for card in hand:
        if card == 'A':
            aces += 1
        elif card in ['K', 'Q', 'J']:
            value += 10
        else:
            value += card
    for i in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1
    return value

# Define a function to play the dealer's turn
def dealer_turn(deck, dealer_hand):
    while calculate_hand(dealer_hand) < 17:
        dealer_hand.append(deck.pop())

# Define a function to simulate the player's decision using basic strategy
def basic_strategy(player_hand, dealer_card):
    player_total = calculate_hand(player_hand)
    if player_total >= 17:
        return 'stand'
    elif player_total <= 11:
        return 'hit'
    elif player_total == 12 and dealer_card in [2, 3, 7, 8, 9, 10, 'A']:
        return 'hit'
    elif player_total in [13, 14, 15, 16] and dealer_card in [2, 3, 4, 5, 6]:
        return 'stand'
    else:
        return 'hit'

# Define a function to play a game of blackjack
def play_blackjack():
    # Shuffle the deck
    random.shuffle(deck)

    # Deal the cards
    dealer_hand = [deck.pop(), deck.pop()]
    player_hand = [deck.pop(), deck.pop()]

    # Play the player's turn using basic strategy
    while basic_strategy(player_hand, dealer_hand[0]) == 'hit':
        player_hand.append(deck.pop())
        if calculate_hand(player_hand) > 21:
            print(f"Bust! Your hand is {player_hand}")
            return 'loss'

    # Play the dealer's turn
    dealer_turn(deck, dealer_hand)

    # Determine the winner
    dealer_value = calculate_hand(dealer_hand)
    player_value = calculate_hand(player_hand)
    if dealer_value > 21 or player_value > dealer_value:
        return 'win'
    elif player_value == dealer_value:
        return 'push'
    else:
        return 'loss'

# Get the number of hands to play from the user
num_hands = int(input("How many hands of blackjack do you want to play? "))

# Play the specified number of games of blackjack
wins = 0
losses = 0
pushes = 0
for i in range(num_hands):
    result = play_blackjack()
    if result == 'win':
        wins += 1
    elif result == 'loss':
        losses += 1
    else:
        pushes += 1

# Output the results
print(f"Wins: {wins}")
print(f"Losses: {losses}")
print(f"Pushes: {pushes}")
