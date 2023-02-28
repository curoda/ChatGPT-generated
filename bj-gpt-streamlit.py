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
def play_blackjack(num_decks, num_hands, can_double, can_surrender, bet, stop):
    global deck
    total_winnings = 0
    num_splits = 0
    num_double_downs = 0
    num_surrenders = 0
    for i in range(num_hands):
         # Check if total_winnings is greater than or equal to the winnings to stop
        if total_winnings >= stop:
            break
        if len(deck) < num_decks * 52 / 4:
            new_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]
        can_split = num_splits < 3 and player_hand[0] == player_hand[1]
        player_busted = False
        while basic_strategy(player_hand, dealer_hand[0]) == 'hit':
            player_hand.append(deck.pop())
            if calculate_hand(player_hand) > 21:
                player_busted = True
                break
        if player_busted:
            total_winnings -= bet
        else:
            # Check for a split
            if can_split:
                num_splits += 1
                player_hand_1 = [player_hand[0], deck.pop()]
                player_hand_2 = [player_hand[1], deck.pop()]
                can_split_1 = num_splits < 3 and player_hand_1[0] == player_hand_1[1]
                can_split_2 = num_splits < 3 and player_hand_2[0] == player_hand_2[1]
                if basic_strategy(player_hand_1, dealer_hand[0]) == 'stand':
                    dealer_turn(dealer_hand)
                else:
                    while basic_strategy(player_hand_1, dealer_hand[0]) == 'hit':
                        player_hand_1.append(deck.pop())
                        if calculate_hand(player_hand_1) > 21:
                            break
                    dealer_turn(dealer_hand)
                if basic_strategy(player_hand_2, dealer_hand[0]) == 'stand':
                    dealer_turn(dealer_hand)
                else:
                    while basic_strategy(player_hand_2, dealer_hand[0]) == 'hit':
                        player_hand_2.append(deck.pop())
                        if calculate_hand(player_hand_2) > 21:
                            break
                    dealer_turn(dealer_hand)
                player_total_1 = calculate_hand(player_hand_1)
                dealer_total = calculate_hand(dealer_hand)
                if player_total_1 > 21:
                    total_winnings -= bet
                elif dealer_total > 21:
                    total_winnings += bet
                elif player_total_1 > dealer_total:
                    total_winnings += bet
                elif player_total_1 < dealer_total:
                    total_winnings -= bet
                # Handle the case of a push (tie)
                else:
                    total_winnings += 0
                player_total_2 = calculate_hand(player_hand_2)
                dealer_total = calculate_hand(dealer_hand)
                if player_total_2 > 21:
                    total_winnings -= bet
                elif dealer_total > 21:
                    total_winnings += bet
                elif player_total_2 > dealer_total:
                    total_winnings += bet

    st.write(f"Winnings: {total_winnings}")
  


# Set up the Streamlit app
st.title("Blackjack Simulator")
num_hands = st.slider("How many hands do you want to play?", min_value=100, max_value=3000, value=200, step=50)
bet = st.slider ("How much do you want to bet per hand?", min_value=10, max_value=100, value=20, step=5)
winings_to_stop = st.slider ("How much do you need to win to stop?", min_value=10, max_value=500, value=100, step=5)
button = st.button("Play")

if button:
    # Play the specified number of games of blackjack
    wins = 0
    losses = 0
    pushes = 0
    result = play_blackjack(num_decks=6, num_hands=num_hands, can_double=True, can_surrender=True, bet=bet, stop=winings_to_stop)
        
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
