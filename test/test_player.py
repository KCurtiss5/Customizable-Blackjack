import pytest
import sys
import os
from unittest.mock import MagicMock
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from Card import Card
from Hand import Hand, Outcome
from Deck import Deck
from Player import Player


class TestPlayer:

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.player = Player("Test", 1000)
        self.three_of_hearts = Card("Hearts", 3)
        self.ten_of_clubs = Card("Clubs", 10)
        self.ace_of_spades = Card("Spades", "Ace")
        self.player.hand = Hand(123, [self.three_of_hearts, self.ten_of_clubs])
        self.deck = Deck(5)

    def test_constructor(self):
        assert self.player

    def test_constructor_with_non_str_name(self):
        with pytest.raises(ValueError):
            self.player = Player(["Not a string","shouldn't work"], 1000)

    def test_constructor_with_non_int_money(self):
        with pytest.raises(ValueError):
            self.player = Player("test", "Non-integer")

    def test_constructor_with_negative_money(self):
        with pytest.raises(ValueError):
            self.player = Player("test", -100)

    def test_variables(self):
        assert self.player.name == "Test"
        assert self.player.money == 1000

    def test_bet(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: "50")
        self.player.bet(5)
        assert self.player.hand.bet == 50

    def test_invalid_bet(self, monkeypatch):
        responses = iter(['50', '250'])
        monkeypatch.setattr('builtins.input', lambda _: next(responses))
        self.player.bet(100)
        assert self.player.hand.bet == 250

    def test_string_representation(self):
        assert str(self.player) == "Test, you have $1000."
    
    def test_stand_is_called(self, monkeypatch):
        mock = Player
        mock.stand = MagicMock()
        monkeypatch.setattr('builtins.input', lambda _: "stand")
        mock.play(self.player, self.deck)
        mock.stand.assert_called_once()
        assert self.player.hand.result == Outcome.UNFINISHED

    def test_stand(self, monkeypatch, capfd):
        monkeypatch.setattr('builtins.input', lambda _: "stand")
        self.player.play(self.deck)
        output, _ = capfd.readouterr()
        #output, _ = capfd.readouterr()
        assert self.player.hand.result == Outcome.UNFINISHED
        assert len(self.player.hand) == 2
        assert "Standing" in output
    
    def test_hit_is_called(self, monkeypatch):
        mock = Player
        mock.hit = MagicMock()
        monkeypatch.setattr('builtins.input', lambda _: "hit")
        mock.play(self.player, self.deck)
        mock.hit.assert_called_once()
        assert self.player.hand.result == Outcome.UNFINISHED

    '''def test_receive_card(self):
        self.three_card_hand.receive_card(self.three_of_hearts)
        assert (len(self.three_card_hand) == 4)

    def test_take_card(self):
        popped_card = self.three_card_hand.take_card()
        assert (popped_card == self.ace_of_spades)
        assert (len(self.three_card_hand) == 2)

    def test_get_score_one_ace(self):
        assert (self.three_card_hand.get_score() == 14)

    def test_get_score_bust(self):
        self.three_card_hand.receive_card(self.ten_of_clubs)
        assert (self.three_card_hand.get_score() == 24)

    def test_get_score_two_aces(self):
        self.three_card_hand.receive_card(self.ace_of_spades)
        self.three_card_hand.receive_card(self.ace_of_spades)
        assert (self.three_card_hand.get_score() == 16)

    def test_get_score_one_ace_gets_to_21(self):
        test_hand = Hand(
            200, [self.ten_of_clubs, self.ace_of_spades, self.ace_of_spades])
        assert (test_hand.get_score() == 12)

    def test_no_card_hand_score(self):
        for _ in range(0, 3):
            self.three_card_hand.take_card()
        assert (self.three_card_hand.get_score() == 0)

    def test_clear_hand(self):
        self.three_card_hand.clear_hand()
        assert len(self.three_card_hand) == 0

    def test_len_dunder(self):
        assert len(self.three_card_hand) == len(self.three_card_hand.cards)'''
