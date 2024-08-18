from enum import Enum, auto
from math import floor
from Card import Card
from helper_functions import get_hand


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
        self.cards = self.bet = self.result = None
        self._initalize(bet, card_list)

    def _initalize(self, bet=0, card_list=None) -> None:
        if card_list and any(not isinstance(card, Card) for card in card_list):
            raise ValueError(f"Error, invalid card_list: {card_list}.")
        if not isinstance(bet, int):
            raise ValueError(f"Error, invalid bet: {bet}.")
        self.cards = card_list if card_list else []
        self.bet = bet
        self.result = Outcome.UNFINISHED

    def set_bet(self, bet) -> None:
        if (not isinstance(bet, int)):
            raise ValueError(f"Error, invalid bet: {bet}.")
        self.bet = bet

    def set_result(self, outcome: Outcome) -> None:
        self.result = outcome

    def clear_hand(self) -> None:
        self._initalize()

    def take_card(self) -> Card:
        return self.cards.pop()

    def receive_card(self, card) -> None:
        if (not isinstance(card, Card)):
            raise ValueError(f"Error, invalid card: {card}.")
        self.cards.append(card)

    def get_score(self) -> int:
        num_aces = 0
        score = 0
        for card in self.cards:
            if card.num != "Ace":
                if isinstance(card.num, int):
                    score += card.num
                else:
                    score += 10
            else:
                num_aces += 1
                score += 1
        for _ in range(0, num_aces):
            if score + 10 <= 21:
                score += 10
        return score
    
    def judge_hand(self, dealer_score: int) -> None:
        if self.result != Outcome.UNFINISHED:
            return
        if dealer_score < self.get_score() or dealer_score > 21:
            self.set_result(Outcome.WIN)
        elif dealer_score > self.get_score():
            self.set_result(Outcome.LOSE)
        else:
            self.set_result(Outcome.PUSH)

    def calculate_payout(self) -> int:
        owed = {Outcome.SURRENEDERED: -0.5, Outcome.NATURAL: 1.5,
                Outcome.WIN: 1, Outcome.PUSH: 0,
                Outcome.BUST: -1, Outcome.LOSE: -1}
        return floor(owed[self.result] * self.bet)  # bust or lose
    
    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, item) -> Card:
        return self.cards[item]

    def __repr__(self) -> str:
        return get_hand(self)
