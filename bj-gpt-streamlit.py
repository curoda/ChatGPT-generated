import random
import streamlit as st

# Create a deck of cards
deck = []

# Define a function to create a new deck
def new_deck():
    global deck
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 24
    random.shuffle(deck)

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
def dealer_turn(dealer_hand):
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
    # Check if the deck needs to be reshuffled
    if len(deck) < 52:
        new_deck()

    # Deal the cards
    dealer_hand = [deck.pop(), deck.pop()]
    player_hand = [deck.pop(), deck.pop()]

    # Play the player's turn using basic strategy
    while basic_strategy(player_hand, dealer_hand[0]) == 'hit':
        player_hand.append(deck.pop())
        if calculate_hand(player_hand) > 21:
            st.write(f"Bust! Your hand is {player_hand}")
            return 'loss'

    # Play the dealer's turn
    dealer_turn(dealer_hand)

    # Determine the winner
    dealer_value = calculate_hand(dealer_hand)
    player_value = calculate_hand(player_hand)
    if dealer_value > 21 or player_value > dealer_value:
        return 'win'
    elif player_value == dealer_value:
        return 'push'
    else:
        return 'loss'

# Set up the Streamlit app
st.title("Blackjack Simulator")
num_hands = st.slider("How many hands do you want to play?", min_value=1, max_value=1000, value=200)
button = st.button("Play")

if button:
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
    st.write(f"Wins: {wins}")
    st.write(f"Losses: {losses}")
    st.write(f"Pushes: {pushes}")
