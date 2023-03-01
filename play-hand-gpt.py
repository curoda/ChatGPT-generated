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
        """
        Calculates the winnings or losses from a single hand of blackjack.

        Args:
        - player_hand: a list representing the player's hand
        - dealer_hand: a list representing the dealer's hand
        - bet_amount: an integer representing the amount bet on the hand

        Returns:
        - An integer representing the winnings or losses from the hand
        """

        # Helper function to recursively calculate winnings for split hands
        def calculate_split_winnings(split_hands, dealer_hand, bet_amount):
            split_winnings = 0
            for split_hand in split_hands:
                if len(split_hand) == 2 and split_hand[0] == "A":
                    # Handle split aces (can only take one additional card per ace)
                    split_hand_new = [split_hand[0], deal_card(deck)]
                    if get_hand_value(split_hand_new) <= 21:
                        split_winnings += calculate_hand_winnings(split_hand_new, dealer_hand, bet_amount)
                    else:
                        split_winnings -= bet_amount
                elif len(split_hand) == 2 and split_hand[0] == split_hand[1]:
                    # Handle another split if applicable
                    split_hands_new = [[split_hand[0], deal_card(deck)], [split_hand[1], deal_card(deck)]]
                    split_winnings += calculate_split_winnings(split_hands_new, dealer_hand, bet_amount)
                else:
                    split_winnings += calculate_hand_winnings(split_hand, dealer_hand, bet_amount)
            return split_winnings

        player_hand_value = get_hand_value(player_hand)
        dealer_hand_value = get_hand_value(dealer_hand)

        if player_hand_value > 21:
            return -bet_amount
        elif dealer_hand_value > 21 or player_hand_value > dealer_hand_value or (player_hand_value == 21 and len(player_hand) == 2 and dealer_hand_value != 21):
            if player_hand_value == 21 and len(player_hand) == 2:
                return int(1.5 * bet_amount)
            else:
                return bet_amount
        elif player_hand_value == dealer_hand_value:
            return 0
        elif len(player_hand) == 2 and player_hand[0] == player_hand[1]:
            split_hands = [[player_hand[0], deal_card(deck)], [player_hand[1], deal_card(deck)]]
            return calculate_split_winnings(split_hands, dealer_hand, bet_amount)
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
        split_hands = [player_hand]
        while len(split_hands) > 0:
            curr_hand = split_hands.pop(0)
            while True:
                action = blackjack_strategy(curr_hand, dealer_hand[0])
                if action == "hit":
                    curr_hand.append(deal_card(deck))
                elif action == "stand":
                    break
                elif action == "double":
                    curr_hand.append(deal_card(deck))
                    bet_amount *= 2
                    break
                elif action == "split":
                    # Split the hand and add the resulting split hands to the list of hands to play
                    hand1 = [curr_hand[0], deal_card(deck)]
                    hand2 = [curr_hand[1], deal_card(deck)]
                    split_hands.extend([hand1, hand2])
                    break
                elif action == "surrender":
                    bet_amount -= 0.5 * bet_amount
                    break

                if get_hand_value(curr_hand) > 21:
                    break

        # Play the dealer's hand
        while get_hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card(deck))

        # Calculate the winnings or losses from the hand(s)
        total_winnings += calculate_hand_winnings(player_hand, dealer_hand, bet_amount)

        num_hands_played += 1

        # Reset the bet amount if it was lowered for a surrender, before playing next hand
        bet_amount = bet_slider

    # Return the total winnings or losses
    return total_winnings


