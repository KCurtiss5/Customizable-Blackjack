import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from Deck import Deck
from Card import Card
from copy import deepcopy

class TestDeck:

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.deck = Deck()
        
    def test_constructor(self):
        assert self.deck

    def test_invalid_deck_num_str(self):
        with pytest.raises(ValueError):
            Deck("test", 5)

    def test_invalid_deck_num_negative(self):
        with pytest.raises(ValueError):
            Deck(-5, 5)

    def test_both_invalid_str(self):
        with pytest.raises(ValueError):
            Deck("test", "test")
    
    def test_invalid_max_turn_str(self):
        with pytest.raises(ValueError):
            Deck(5, "test")
    
    def test_invalid_max_turn_negative(self):
        with pytest.raises(ValueError):
            Deck(5, -5)

    def test_deck_length_one_deck(self):
        assert(len(self.deck.deck) == 52)

    def test_deck_length_five_decks(self):
        self.deck = Deck(5)
        assert(len(self.deck.deck) == 260)

    def test_deck_length_fivethousand_decks(self):
        self.deck = Deck(5000)
        assert(len(self.deck.deck) == 260000)

    def test_a_few_cards_in_deck(self):
        assert (Card("Hearts",5) in self.deck.deck)
        assert (Card("Clubs","Ace") in self.deck.deck)
        assert (Card("Diamonds",10) in self.deck.deck)
        assert (Card("Spades","Queen") in self.deck.deck)

    def test_shuffle_after_1_turn(self, capfd):
        self.deck.increment_turn_count()
        output, _ = capfd.readouterr()
        assert ("Shuffling deck..." in output)

    def test_shuffle_after_5_turns(self, capfd):
        for _ in range(0,5):
            self.deck.increment_turn_count()
        output, _ = capfd.readouterr()
        assert (output.count("Shuffling deck...")==5)

    def test_shuffle(self):
        orig_deck = deepcopy(self.deck.deck)
        self.deck.shuffle()
        assert (orig_deck != self.deck.deck)

    def test_deal_card(self):
        card = self.deck.deal_card()
        assert card
        assert len(self.deck.deck) == 51
        assert len(self.deck.used_cards) == 1

    def test_deal_30_cards(self):
        card_list = []
        for _ in range(0,30):
            card_list.append(self.deck.deal_card())
        assert len(card_list) == 30
        assert len(self.deck.deck) == 22
        assert len(self.deck.used_cards) == 30
    
    def test_deal_30_cards_then_shuffle(self):
        card_list = []
        for _ in range(0,30):
            card_list.append(self.deck.deal_card())
        assert len(card_list) == 30
        assert len(self.deck.deck) == 22
        assert len(self.deck.used_cards) == 30
        self.deck.increment_turn_count()
        assert len(self.deck.deck) == 52
        assert len(self.deck.used_cards) == 0

