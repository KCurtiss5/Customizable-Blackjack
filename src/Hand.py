from Card import Card
from helper_functions import get_hand


class Hand:
    def __init__(self, bet: int, card_list=[]) -> None:
        if any(not isinstance(card, Card) for card in card_list):
            raise ValueError(f"Error, invalid card_list: {card_list}.")
        self.cards = card_list
        if (not isinstance(bet, int)):
            raise ValueError(
                f"Error, invalid bet: {bet}.")
        self.bet = bet

    def clear_hand(self) -> None:
        self.__init__(0)

    def take_card(self) -> Card:
        card = self.cards.pop()
        return card

    def receive_card(self, card: Card) -> None:
        self.cards.append(card)

    def get_score(self) -> int:
        self.numAce = 0
        score = 0
        for card in self.cards:
            if (card.num != "Ace"):
                if (isinstance(card.num, int)):
                    score += card.num
                else:
                    score += 10
            else:
                self.numAce += 1
                score += 1
        for _ in range(0, self.numAce):
            if (score + 10 <= 21):
                score += 10
        return score

    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, item) -> Card:
        return self.cards[item]

    def __repr__(self) -> str:
        return get_hand(self)
