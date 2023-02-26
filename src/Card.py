class Card:
    def __init__(self, suit: str, num):
        if not self._validate_suit(suit):
            raise ValueError(f"Cannot create card, invalid suit name {suit}")
        if not self._validate_num(num):
            raise ValueError("Cannot create card, invalid num ", num)

        self._suit = suit
        self._num = num

    def _validate_suit(self, suit: str) -> bool:
        return suit in ["Hearts", "Diamonds", "Clubs", "Spades"]

    def _validate_num(self, num) -> bool:
        if (isinstance(num, int)):
            return num >= 2 and num <= 10
        return num in ["Ace", "Jack", "Queen", "King"]

    def get_suit(self):
        return self._suit

    def get_num(self):
        return self._num

    def __str__(self):
        return f"{self._num} of {self._suit}"
