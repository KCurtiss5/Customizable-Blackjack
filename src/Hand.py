from enum import Enum, auto
from Card import Card
from helper_functions import get_hand
from math import floor


class Outcome(Enum):
    UNFINISHED = auto()
    SURRENEDERED = auto()
    NATURAL = auto()
    WIN = auto()
    PUSH = auto()
    BUST = auto()
    LOSE = auto()


class Hand:
    def __init__(self, bet=0, card_list=None) -> None:
        if card_list and any(not isinstance(card, Card) for card in card_list):
            raise ValueError(f"Error, invalid card_list: {card_list}.")
        if (not isinstance(bet, int)):
            raise ValueError(
                f"Error, invalid bet: {bet}.")
        self.cards = card_list if card_list else []
        self.bet = bet
        self.result = Outcome.UNFINISHED

    def set_bet(self, bet: int):
        self.bet = bet

    def set_result(self, outcome: Outcome):
        self.result = outcome

    def clear_hand(self) -> None:
        self.__init__(0)

    def take_card(self) -> Card:
        return self.cards.pop()

    def receive_card(self, card: Card) -> None:
        self.cards.append(card)

    def get_score(self) -> int:
        self.num_aces = 0
        score = 0
        for card in self.cards:
            if (card.num != "Ace"):
                if (isinstance(card.num, int)):
                    score += card.num
                else:
                    score += 10
            else:
                self.num_aces += 1
                score += 1
        for _ in range(0, self.num_aces):
            if (score + 10 <= 21):
                score += 10
        return score

    def money_owed(self) -> int:
        if self.result == Outcome.SURRENEDERED:
            return floor(-0.5 * self.bet)
        elif self.result == Outcome.NATURAL:
            return floor(1.5 * self.bet)
        elif self.result == Outcome.WIN:
            return floor(1 * self.bet)
        elif self.result == Outcome.PUSH:
            return 0
        else:  # bust or lose
            return floor(-1 * self.bet)

    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, item) -> Card:
        return self.cards[item]

    def __repr__(self) -> str:
        return get_hand(self)
