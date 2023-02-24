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
def basic_strategy(player_hand, dealer_card, num_splits, can_double, can_surrender):
    player_total = calculate_hand(player_hand)
    if num_splits > 0 and player_hand[0] == player_hand[1]:
        if player_hand[0] in [2, 3] and dealer_card in [2, 3, 4, 5, 6, 7]:
            return 'split'
        elif player_hand[0] in [4, 5] and dealer_card in [2, 3, 4, 5, 6]:
            return 'split'
        elif player_hand[0] == 6 and dealer_card in [2, 3, 4, 5, 6]:
            return 'split'
        elif player_hand[0] == 7 and dealer_card in [2, 3, 4, 5, 6]:
            return 'split' if num_splits < 3 else 'hit'
        elif player_hand[0] == 8 and dealer_card in [2, 3, 4, 5, 6]:
            return 'split'
        elif player_hand[0] == 9 and dealer_card in [2, 3, 4, 5, 6, 8, 9]:
            return 'split' if num_splits < 3 else 'stand'
        elif player_hand[0] == 10 and dealer_card in [2, 3, 4, 5, 6, 7, 8, 9]:
            return 'split'
        elif player_hand[0] == 'A' and dealer_card in [2, 3, 4, 5, 6, 8, 9, 10, 'A']:
            return 'split' if num_splits < 3 else 'stand'
    if can_double and player_total in [9, 10, 11]:
        if player_total == 9 and dealer_card in [2, 3, 4, 5, 6, 8, 9]:
            return 'double'
        elif player_total == 10 and dealer_card in [2, 3, 4, 5, 6, 7, 8, 9]:
            return 'double'
        elif player_total == 11 and dealer_card in [2, 3, 4, 5, 6, 7, 8, 9, 10, 'A']:
            return 'double'
    if can_surrender and player_total in [15, 16]:
        if player_total == 15 and dealer_card in [9, 10, 'A']:
            return 'surrender'
        elif player_total == 16 and dealer_card in [9, 10, 'A', 7]:
            return 'surrender'
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
def play_blackjack(num_decks, num_hands, can_double, can_surrender):
    global deck
    total_winnings = 0
    num_splits = 0
    num_double_downs = 0
    num_surrenders = 0
    for i in range(num_hands):
         # Check if total_winnings is greater than or equal to 20
        if total_winnings >= 20:
            break
        if len(deck) < num_decks * 52 / 4:
            new_deck()
        dealer_hand = [deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]
        can_split = num_splits < 3 and player_hand[0] == player_hand[1]
        player_busted = False
        while basic_strategy(player_hand, dealer_hand[0], num_splits, can_double, can_surrender) == 'hit':
            player_hand.append(deck.pop())
            if calculate_hand(player_hand) > 21:
                player_busted = True
                break
        if player_busted:
            total_winnings -= 10
        else:
            # Check for a split
            if can_split:
                num_splits += 1
                player_hand_1 = [player_hand[0], deck.pop()]
                player_hand_2 = [player_hand[1], deck.pop()]
                can_split_1 = num_splits < 3 and player_hand_1[0] == player_hand_1[1]
                can_split_2 = num_splits < 3 and player_hand_2[0] == player_hand_2[1]
                if basic_strategy(player_hand_1, dealer_hand[0], num_splits, can_double, can_surrender) == 'stand':
                    dealer_turn(dealer_hand)
                else:
                    while basic_strategy(player_hand_1, dealer_hand[0], num_splits, can_double, can_surrender) == 'hit':
                        player_hand_1.append(deck.pop())
                        if calculate_hand(player_hand_1) > 21:
                            break
                    dealer_turn(dealer_hand)
                if basic_strategy(player_hand_2, dealer_hand[0], num_splits, can_double, can_surrender) == 'stand':
                    dealer_turn(dealer_hand)
                else:
                    while basic_strategy(player_hand_2, dealer_hand[0], num_splits, can_double, can_surrender) == 'hit':
                        player_hand_2.append(deck.pop())
                        if calculate_hand(player_hand_2) > 21:
                            break
                    dealer_turn(dealer_hand)
                player_total_1 = calculate_hand(player_hand_1)
                dealer_total = calculate_hand(dealer_hand)
                if player_total_1 > 21:
                    total_winnings -= 10
                elif dealer_total > 21:
                    total_winnings += 10
                elif player_total_1 > dealer_total:
                    total_winnings += 10
                elif player_total_1 < dealer_total:
                    total_winnings -= 10
                # Handle the case of a push (tie)
                else:
                    total_winnings += 0
                player_total_2 = calculate_hand(player_hand_2)
                dealer_total = calculate_hand(dealer_hand)
                if player_total_2 > 21:
                    total_winnings -= 10
                elif dealer_total > 21:
                    total_winnings += 10
                elif player_total_2 > dealer_total:
                    total_winnings += 10

    st.write(f"Winnings: {total_winnings}")
  


# Set up the Streamlit app
st.title("Blackjack Simulator")
num_hands = st.slider("How many hands do you want to play?", min_value=1, max_value=1000, value=200)
button = st.button("Play")

if button:
    # Play the specified number of games of blackjack
    wins = 0
    losses = 0
    pushes = 0
    result = play_blackjack(num_decks=6, num_hands=num_hands, can_double=True, can_surrender=True)
        
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
