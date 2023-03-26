from Card import Card
from random import shuffle

class Deck:
    def __init__(self, deck_num=1, max_turns=1):
        self.deck_num = deck_num
        self.deck = []
        self.used_cards = []
        self.shuffle()
        self.max_turns = max_turns
        self.turn_counter = 0

    def build_deck(self) -> None:
        deck = []
        for _ in range(0, self.deck_num):
            for x in ["Spades", "Clubs", "Diamonds", "Hearts"]:
                for y in range(2, 11):
                    deck.append(Card(x, y))
                for y in ["Jack", "Queen", "King", "Ace"]:
                    deck.append(Card(x, y))
        return deck
    
    def increment_turn_count(self):
        self.turn_counter+=1
        if (self.turn_counter >= self.max_turns):
            self.turn_counter = 0
            self.shuffle()

    def shuffle(self) -> None:
        print("Shuffling deck...")
        self.deck = self.build_deck()
        shuffle(self.deck)
        return

    def deal_card(self):
        if (len(self.deck) == 0):
            self.shuffle()
            self.turn_counter = 0
        card = self.deck.pop(0)
        self.used_cards.append(card)
        return (card)