import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from Card import Card
from Hand import Hand
from Player import Dealer

class TestDealer:

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.dealer = Dealer()
        self.three_of_hearts = Card("Hearts", 3)
        self.ten_of_clubs = Card("Clubs", 10)
        self.ace_of_spades = Card("Spades", "Ace")
        self.hand = Hand(
            0, [self.three_of_hearts, self.three_of_hearts, self.ten_of_clubs, self.ace_of_spades])
        self.dealer.hand = self.hand
        
    def test_constructor(self):
        assert self.dealer

    def test_invalid_constructor_ValueError(self):
        with pytest.raises(ValueError):
            self.dealer = Dealer(500)

    def test_invalid_constructor_TypeError(self):
        with pytest.raises(TypeError):
            self.dealer = Dealer(500, 500, 500)

    def test_constructor_with_boolean(self):
        self.dealer = Dealer(True)
        assert self.dealer
    
    def test_dealer_S17(self):
        assert self.dealer.hand.get_score() == 17
        assert not self.dealer.should_dealer_hit()

    def test_dealer_H17(self):
        self.dealer = Dealer(True)
        self.dealer.hand = self.hand
        assert self.dealer.hand.get_score() == 17
        assert self.dealer.should_dealer_hit()

    def test_dealer_hit_under_17(self):
        self.dealer.hand = Hand(0, [self.three_of_hearts, self.ten_of_clubs])
        assert self.dealer.should_dealer_hit()

    def test_dealer_not_hit_over_17(self):
        self.dealer.hand = Hand(0, [self.ten_of_clubs, self.ace_of_spades])
        assert not self.dealer.should_dealer_hit()

    def test_dealer_reveal(self):
        assert len(self.dealer.reveal().split("\n")) == 8
        assert "Dealer has" in self.dealer.reveal()
        assert '>' in self.dealer.reveal()

