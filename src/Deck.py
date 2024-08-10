from random import shuffle
from Card import Card


class Deck:
    def __init__(self, deck_num=1, max_turns=1):
        if not isinstance(deck_num, int) or deck_num <= 0:
            raise ValueError(f"Error, invalid deck_num: {deck_num}.")
        if not isinstance(max_turns, int) or max_turns <= 0:
            raise ValueError(f"Error, invalid max_turns: {max_turns}.")
        self.deck_num = deck_num
        self.max_turns = max_turns
        self.deck = self.build_deck()
        self.used_cards = []
        self.turn_counter = 0
        self.shuffle()

    def build_deck(self) -> list:
        deck = []
        for _ in range(0, self.deck_num):
            for x in ["Spades", "Clubs", "Diamonds", "Hearts"]:
                for y in range(2, 11):
                    deck.append(Card(x, y))
                for y in ["Jack", "Queen", "King", "Ace"]:
                    deck.append(Card(x, y))
        return deck

    def increment_turn_count(self) -> None:
        self.turn_counter += 1
        if self.turn_counter >= self.max_turns:
            self.turn_counter = 0
            self.shuffle()

    def shuffle(self) -> None:
        print("Shuffling deck...")
        self.deck = self.deck + self.used_cards
        self.used_cards = []
        shuffle(self.deck)

    def deal_card(self) -> Card:
        if len(self.deck) == 0:
            self.shuffle()
            self.turn_counter = 0
        card = self.deck.pop(0)
        self.used_cards.append(card)
        return card
