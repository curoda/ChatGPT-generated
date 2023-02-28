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

