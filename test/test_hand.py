import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from card import Card
from hand import Hand


class TestHand:

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.three_of_hearts = Card("Hearts", 3)
        self.ten_of_clubs = Card("Clubs", 10)
        self.ace_of_spades = Card("Spades", "Ace")
        self.three_card_hand = Hand(
            500, [self.three_of_hearts, self.ten_of_clubs, self.ace_of_spades])

    def test_constructor(self):
        assert self.three_card_hand

    def test_constructor_with_invalid_bet(self):
        with pytest.raises(ValueError):
            Hand("test", [])

    def test_constructor_with_invalid_card_list(self):
        self.three_of_hearts = "test"
        with pytest.raises(ValueError):
            self.three_card_hand = Hand(
                500, [self.three_of_hearts, self.ten_of_clubs, self.ace_of_spades])

    def test_variables(self):
        assert self.three_card_hand.bet == 500
        assert len(self.three_card_hand) == 3

    def test_str(self):
        assert len(str(self.three_card_hand).split("\n")) == 7
        assert str(self.three_card_hand).count('\u2665') == 3  # 3 hearts
        assert str(self.three_card_hand).count('\u2663') == 10  # 10 clubs
        assert str(self.three_card_hand).count('\u2660') == 1  # and a spade

    def test_receive_card(self):
        self.three_card_hand.receive_card(self.three_of_hearts)
        assert len(self.three_card_hand) == 4

    def test_take_card(self):
        popped_card = self.three_card_hand.take_card()
        assert popped_card == self.ace_of_spades
        assert len(self.three_card_hand) == 2

    def test_get_score_one_ace(self):
        assert self.three_card_hand.get_score() == 14

    def test_get_score_bust(self):
        self.three_card_hand.receive_card(self.ten_of_clubs)
        assert self.three_card_hand.get_score() == 24

    def test_get_score_two_aces(self):
        self.three_card_hand.receive_card(self.ace_of_spades)
        self.three_card_hand.receive_card(self.ace_of_spades)
        assert self.three_card_hand.get_score() == 16

    def test_get_score_one_ace_gets_to_21(self):
        test_hand = Hand(
            200, [self.ten_of_clubs, self.ace_of_spades, self.ace_of_spades])
        assert test_hand.get_score() == 12

    def test_no_card_hand_score(self):
        for _ in range(0, 3):
            self.three_card_hand.take_card()
        assert self.three_card_hand.get_score() == 0

    def test_clear_hand(self):
        self.three_card_hand.clear_hand()
        assert len(self.three_card_hand) == 0

    def test_len_dunder(self):
        assert len(self.three_card_hand) == len(self.three_card_hand.cards)
