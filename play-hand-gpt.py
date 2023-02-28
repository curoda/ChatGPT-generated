import random

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

    # Create a deck of cards
    deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 4

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
        if player_hand_value > 21:
            return -bet_amount
        elif dealer_hand_value > 21 or player_hand_value > dealer_hand_value:
            return bet_amount
        elif player_hand_value == dealer_hand_value:
            return 0
        else:
            return -bet_amount

    # Play multiple hands of blackjack
    total_winnings = 0
    num_hands_played = 0
    while num_hands_played < num_hands and total_winnings >= -max_loss_amount and total_winnings <= min_win_amount:
        # Shuffle the deck
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
        winnings = calculate_hand_winnings(player_hand, dealer_hand)
        total_winnings += winnings
        num_hands_played += 1

    # Return the total winnings or losses
    return total_winnings
