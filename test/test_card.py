import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from card import Card


class TestCard:

    three_of_hearts = Card("Hearts", 3)
    ten_of_clubs = Card("Clubs", 10)
    ace_of_spades = Card("Spades", "Ace")

    def test_constructor(self):
        assert self.three_of_hearts
        assert self.ten_of_clubs
        assert self.ace_of_spades

    def test_variables(self):
        assert self.three_of_hearts.suit == "Hearts"
        assert self.three_of_hearts.num == 3

    def test_str_card_number(self):
        assert len(str(self.three_of_hearts).split("\n")) == 6
        assert str(self.three_of_hearts).count('\u2665') == 3

    def test_str_card_face_card(self):
        assert len(str(self.ace_of_spades).split("\n")) == 6
        assert str(self.ace_of_spades).count('\u2660') == 1

    def test_invalid_suit(self):
        with pytest.raises(ValueError):
            Card("Wrong", 5)

    def test_invalid_suit_2(self):
        with pytest.raises(ValueError):
            Card("Heart", 5)

    def test_invalid_suit_3(self):
        with pytest.raises(ValueError):
            Card("", 5)

    def test_invalid_num_high(self):
        with pytest.raises(ValueError):
            Card("Hearts", 11)

    def test_invalid_num_low(self):
        with pytest.raises(ValueError):
            Card("Hearts", 1)

    def test_invalid_num_huge(self):
        with pytest.raises(ValueError):
            Card("Hearts", 1000)

    def test_invalid_num_string(self):
        with pytest.raises(ValueError):
            Card("Hearts", "Wrong")
