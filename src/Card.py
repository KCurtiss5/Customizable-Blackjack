from helper_functions import get_card


class Card:
    def __init__(self, suit: str, num):
        if not self._validate_suit(suit):
            raise ValueError(f"Error, invalid suit name: {suit}")
        if not self._validate_num(num):
            raise ValueError(f"Error, invalid num: {num}")

        self.suit = suit
        self.num = num

    def _validate_suit(self, suit: str) -> bool:
        return suit in ["Hearts", "Diamonds", "Clubs", "Spades"]

    def _validate_num(self, num) -> bool:
        if (isinstance(num, int)):
            return num >= 2 and num <= 10
        return num in ["Ace", "Jack", "Queen", "King"]

    def __str__(self):
        return f"{get_card(self)}"
