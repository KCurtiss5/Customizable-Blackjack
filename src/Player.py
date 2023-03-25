from Hand import Hand
from abc import ABC, abstractmethod
from helper_functions import get_hand


class Person(ABC):
    @abstractmethod
    def __init__(self):
        self.hand = Hand(0)


class Dealer(Person):
    def __init__(self, H17=False):
        Person.__init__(self)
        if (not isinstance(H17, bool)):
            raise ValueError(
                f"Error, invalid H17: {H17}.")
        self.H17 = H17  # if true, we hit on 17. Else we stand.

    def should_dealer_hit(self):
        score = self.hand.get_score()
        return self.H17 if score == 17 else score < 17

    def reveal(self):
        return f"Dealer has\n{get_hand(self.hand, True)}"
