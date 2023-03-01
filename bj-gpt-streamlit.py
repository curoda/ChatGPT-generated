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
        
# Helper function to get the value of a card
def get_card_value(card):
    if card in ["J", "Q", "K"]:
        return 10
    elif card == "A":
        return 11
    else:
        return int(card)

# Helper function to get the value of a hand
def get_hand_value(hand):
    value = sum(get_card_value(card) for card in hand)
    if value > 21 and "A" in hand:
        value -= 10
    return value

# Define a function to simulate the player's decision using basic strategy
def blackjack_strategy(player_hand, dealer_card):
    """
    Implements a perfect blackjack strategy based on the player's hand and the dealer's up card.
    Args:
    - player_hand: a list of strings representing the player's hand, e.g. ["A", "5"]
    - dealer_card: a string representing the dealer's up card, e.g. "10"
    Returns:
    - A string representing the recommended action, one of "stand", "hit", "split", "double", or "surrender"
    """

    # Helper functions to check if the player's hand is a soft hand or a pair
    def is_soft_hand(hand):
        return any(card == "A" for card in hand) and sum(get_card_value(card) for card in hand) <= 11

    def is_pair(hand):
        return len(hand) == 2 and hand[0] == hand[1]

    # Helper function to check if a hand can be doubled
    def can_double(hand):
        return len(hand) == 2

    # Helper function to check if a hand can be split
    def can_split(hand):
        return len(hand) == 2 and hand[0] == hand[1]

    # Implement the rules for surrender
    if len(player_hand) == 2 and is_soft_hand(player_hand):
        if get_hand_value(player_hand) == 15 and dealer_card in ["10", "J", "Q", "K"]:
            return "surrender"
        elif get_hand_value(player_hand) == 16 and dealer_card in ["9", "10", "J", "Q", "K", "A"]:
            return "surrender"

    # Implement the rules for pairs
    if can_split(player_hand):
        if player_hand[0] == "A":
            return "split"
        elif player_hand[0] == "8":
            return "split"
        elif player_hand[0] == "7" and dealer_card in ["2", "3", "4", "5", "6", "7"]:
            return "split"
        elif player_hand[0] == "6" and dealer_card in ["2", "3", "4", "5", "6"]:
            return "split"
        elif player_hand[0] == "5" and dealer_card in ["2", "3", "4", "5", "6", "7", "8", "9"]:
            return "double"
        elif player_hand[0] == "4" and dealer_card in ["5", "6"]:
            return "split"
        elif player_hand[0] == "3" and dealer_card in ["2", "3", "4", "5", "6", "7"]:
            return "split"
        elif player_hand[0] == "2" and dealer_card in ["2", "3", "4", "5", "6", "7"]:
            return "split"
        elif player_hand[0] == "9" and dealer_card in ["2", "3", "4", "5", "6", "8", "9"]:
            return "stand"
          
    # Implement the rules for soft hands
    if is_soft_hand(player_hand):
        if get_hand_value(player_hand) == 20:
            return "stand"
        elif get_hand_value(player_hand) == 19 and dealer_card == "6":
            return "double"
        elif get_hand_value(player_hand) == 19 and dealer_card != "6":
            return "stand"
        elif get_hand_value(player_hand) == 18 and dealer_card in ["2", "3", "4", "5", "6"]:
            return "double"
        elif get_hand_value(player_hand) == 18 and dealer_card in ["9", "10", "J", "Q", "K", "A"]:
            return "hit"
        elif get_hand_value(player_hand) == 18 and dealer_card in ["7", "8"]:
            return "stand"
        elif get_hand_value(player_hand) == 17 and dealer_card in ["3", "4", "5", "6"]:
            return "double"
        elif get_hand_value(player_hand) == 16 and dealer_card in ["4", "5", "6"]:
            return "double"
        elif get_hand_value(player_hand) == 15 and dealer_card in ["4", "5", "6"]:
            return "double"
        elif get_hand_value(player_hand) == 14 and dealer_card in ["5", "6"]:
            return "double"
        elif get_hand_value(player_hand) == 13 and dealer_card in ["5", "6"]:
            return "double"
        else:
            return "hit"

    # Implement the rules for hard hands
    if get_hand_value(player_hand) >= 17:
        return "stand"
    elif get_hand_value(player_hand) == 16 and dealer_card in ["2", "3", "4", "5", "6"]:
        return "stand"
    elif get_hand_value(player_hand) == 15 and dealer_card in ["2", "3", "4", "5", "6"]:
        return "stand"
    elif get_hand_value(player_hand) == 14 and dealer_card in ["2", "3", "4", "5", "6"]:
        return "stand"
    elif get_hand_value(player_hand) == 13 and dealer_card in ["2", "3", "4", "5", "6"]:
        return "stand"
    elif get_hand_value(player_hand) == 12 and dealer_card in ["4", "5", "6"]:
        return "stand"
    elif get_hand_value(player_hand) == 11:
        if can_double(player_hand):
            return "double"
        else:
            return "hit"
    elif get_hand_value(player_hand) == 10:
        if can_double(player_hand) and dealer_card in ["2", "3", "4", "5", "6", "7", "8", "9"]:
            return "double"
        else:
            return "hit"
    elif get_hand_value(player_hand) == 9:
        if can_double(player_hand) and dealer_card in ["3", "4", "5", "6"]:
            return "double"
        else:
            return "hit"
    else:
        return "hit"


# Define a function to play a game of blackjack
def play_blackjack(num_hands, bet_amount, min_win_amount, max_loss_amount):
    """
    Plays multiple hands of blackjack using a perfect strategy and returns the total winnings.
    Args:
    - num_hands: an integer representing the number of hands to play
    - bet_amount: an integer representing the amount to bet on each hand
    - min_win_amount: an integer representing the minimum amount to win before stopping
    - max_loss_amount: an integer representing the maximum amount to lose before stopping
    Returns:
    - An integer representing the total winnings or losses
    """

    # Create a deck of cards (hardcoded in a 6 deck shuffle)
    deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 24

    # Helper function to shuffle the deck
    def shuffle_deck(deck):
        random.shuffle(deck)

    # Helper function to deal a card
    def deal_card(deck):
        return deck.pop()

    # Helper function to calculate the winnings or losses from a single hand
    def calculate_hand_winnings(player_hand, dealer_hand, bet_amount):
        player_hand_value = get_hand_value(player_hand)
        dealer_hand_value = get_hand_value(dealer_hand)
        st.write(f"player hand value: {player_hand_value}")
        st.write(f"dealer hand value: {dealer_hand_value}")
        if player_hand_value > 21:
            return -bet_amount
        elif dealer_hand_value > 21 or player_hand_value > dealer_hand_value or (player_hand_value == 21 and len(player_hand) == 2 and dealer_hand_value != 21):
            if player_hand_value == 21 and len(player_hand) == 2:
                return int(1.5 * bet_amount)
            else:
                return bet_amount
        elif player_hand_value == dealer_hand_value:
            return 0
        else:
            return -bet_amount


    # Play multiple hands of blackjack
    total_winnings = 0
    num_hands_played = 0
    shuffle_deck(deck)
    while num_hands_played < num_hands and total_winnings >= -max_loss_amount and total_winnings <= min_win_amount:
        # Shuffle the deck (hardcoded in a 6 deck shuffle)
        if len(deck) < 6 * 52 / 4:
            shuffle_deck(deck)

        # Deal the player's and dealer's initial hands
        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck), deal_card(deck)]

        # Play the player's hand
        while True:
            action = blackjack_strategy(player_hand, dealer_hand[0])
            if action == "hit":
                player_hand.append(deal_card(deck))
            elif action == "stand":
                break
            elif action == "double":
                player_hand.append(deal_card(deck))
                bet_amount *= 2
                break
            elif action == "split":
                hand1 = [player_hand[0], deal_card(deck)]
                hand2 = [player_hand[1], deal_card(deck)]
                winnings1 = calculate_hand_winnings(hand1, dealer_hand, bet_amount)
                winnings2 = calculate_hand_winnings(hand2, dealer_hand, bet_amount)
                total_winnings += winnings1 + winnings2
                num_hands_played += 2
                break
            elif action == "surrender":
                total_winnings -= 0.5 * bet_amount
                num_hands_played += 1
                break

            if get_hand_value(player_hand) > 21:
                total_winnings -= bet_amount
                num_hands_played += 1
                break

        # Play the dealer's hand
        while get_hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card(deck))

        # Calculate the winnings or losses from the hand
        winnings = calculate_hand_winnings(player_hand, dealer_hand, bet_amount)
        st.write(f"Hand result: {winnings}")
        total_winnings += winnings
        st.write(f"Total: {total_winnings}")
        num_hands_played += 1

    # Return the total winnings or losses
    st.write(f"Winnings: {total_winnings}")
    total_winnings = 0


# Set up the Streamlit app
st.title("Blackjack Simulator")
num_hands_slider = st.slider("How many hands do you want to play?", min_value=100, max_value=3000, value=200, step=50)
bet_slider = st.slider ("How much do you want to bet per hand?", min_value=10, max_value=100, value=20, step=5)
min_win_slider = st.slider ("How much do you need to win to stop?", min_value=10, max_value=500, value=100, step=5)
max_loss_slider = st.slider ("How much do you need to lose to stop?", min_value=100, max_value=500, value=200, step=50)
button = st.button("Play")

if button:
    # Play the specified number of games of blackjack
    wins = 0
    losses = 0
    pushes = 0
    result = play_blackjack(num_hands=num_hands_slider, bet_amount=bet_slider, min_win_amount=min_win_slider, max_loss_amount=max_loss_slider)
        
   # for i in range(num_hands):
    #    result = play_blackjack(num_decks=6, num_hands=num_hands, can_double=True, can_surrender=True)
     #   if result == 'win':
      #      wins += 1
       # elif result == 'loss':
        #    losses += 1
       # else:
        #    pushes += 1

    # Output the results
    # st.write(f"Wins: {wins}")
    # st.write(f"Losses: {losses}")
    # st.write(f"Pushes: {pushes}")
