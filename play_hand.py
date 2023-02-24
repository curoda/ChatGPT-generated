import csv

def play_blackjack(deck, strategy_file='blackjack_strategy.csv', bet=10):
    # Load the strategy chart from the CSV file
    with open(strategy_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        strategy_chart = list(reader)

    # Deal the initial hands
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Check for player blackjack
    if get_card_value(player_hand) == 21:
        if get_card_value(dealer_hand) != 21:
            return bet * 1.5
        else:
            return 0

    # Play the player's hand
    while get_card_value(player_hand) < 21:
        player_total = get_card_value(player_hand)
        dealer_card = get_card_value([dealer_hand[0]])

        # Get the recommended action from the strategy chart
        action = strategy_chart[player_total-8][dealer_card-2]

        if action == 'hit':
            player_hand.append(deck.pop())
        elif action == 'stand':
            break
        elif action == 'double':
            bet *= 2
            player_hand.append(deck.pop())
            break
        elif action == 'split':
            # Split the hand and play each hand separately
            bet *= 2
            hand1 = [player_hand[0], deck.pop()]
            hand2 = [player_hand[1], deck.pop()]
            outcome1 = play_hand(hand1, dealer_hand, deck, strategy_chart, bet)
            outcome2 = play_hand(hand2, dealer_hand, deck, strategy_chart, bet)
            return outcome1 + outcome2

    # Play the dealer's hand
    while get_card_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())

    # Determine the outcome of the game
    player_total = get_card_value(player_hand)
    dealer_total = get_card_value(dealer_hand)

    if player_total > 21:
        return -bet
    elif dealer_total > 21:
        return bet
    elif player_total > dealer_total:
        return bet
    elif player_total == dealer_total:
        return 0
    else:
        return -bet

def play_hand(player_hand, dealer_hand, deck, strategy_chart, bet):
    # Play the player's hand
    while get_card_value(player_hand) < 21:
        player_total = get_card_value(player_hand)
        dealer_card = get_card_value([dealer_hand[0]])

        # Get the recommended action from the strategy chart
        action = strategy_chart[player_total-8][dealer_card-2]

        if action == 'hit':
            player_hand.append(deck.pop())
        elif action == 'stand':
            break
        elif action == 'double':
            bet *= 2
            player_hand.append(deck.pop())
            break
        elif action == 'split':
            # Split the hand and play each hand separately
            bet *= 2
            hand1 = [player_hand[0], deck.pop()]
            hand2 = [player_hand[1], deck.pop()]
            outcome1 = play_hand(hand1, dealer_hand, deck, strategy_chart, bet)
            outcome2 = play_hand(hand2, dealer_hand, deck, strategy_chart, bet)
            return outcome1 + outcome2

    # Play the dealer's hand
    while get_card_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())

    # Determine the outcome of the game
    player_total = get_card_value(player_hand)
    dealer_total = get_card_value(dealer_hand)

    if player_total > 21:
        return -bet
    elif dealer_total > 21:
        return bet
    elif player_total > dealer_total:
        return bet
    elif player_total == dealer_total:
        return 0
    else:
        return -bet
