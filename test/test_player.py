from unittest.mock import patch
import os
import sys
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from Card import Card
from Deck import Deck
from Hand import Hand, Outcome
from Player import Player

INPUT = "builtins.input"

class TestPlayer:

    three_of_hearts = Card("Hearts", 3)
    ten_of_clubs = Card("Clubs", 10)
    eight_of_diamonds = Card("Diamonds", 8)
    ace_of_spades = Card("Spades", "Ace")

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.player = Player("Test", 1000)
        self.player.hand = Hand(123, [self.three_of_hearts, self.ten_of_clubs])
        self.deck = Deck(1)
        self.add_eight = Deck(1, 1, [self.eight_of_diamonds])
        self.add_three = Deck(1, 1, [self.three_of_hearts])
        self.add_ten = Deck(1, 1, [self.ten_of_clubs])

    def test_constructor(self):
        assert self.player

    def test_constructor_with_non_str_name(self):
        with pytest.raises(ValueError):
            self.player = Player(["Not a string", "shouldn't work"], 1000)

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
        monkeypatch.setattr(INPUT, lambda _: "50")
        self.player.bet(5)
        assert self.player.hand.bet == 50

    def test_invalid_bet(self, monkeypatch):
        responses = iter(['50', '250'])
        monkeypatch.setattr(INPUT, lambda _: next(responses))
        self.player.bet(100)
        assert self.player.hand.bet == 250

    def test_string_representation(self):
        assert str(self.player) == "Test, you have $1000."

    def test_hit(self):
        self.player.hit(self.player.hand, self.add_three, False) #should be 16
        assert self.player.hand.result == Outcome.UNFINISHED
        assert len(self.player.hand) == 3

    def test_hit_until_bust(self):
        self.player.hit(self.player.hand, self.add_three, False) #should be 16
        assert self.player.hand.result == Outcome.UNFINISHED
        assert len(self.player.hand) == 3
        self.player.hit(self.player.hand, self.add_eight) #should be 24
        assert self.player.hand.result == Outcome.BUST
        assert len(self.player.hand) == 4

    def test_hit_with_21(self, capsys):
        self.player.hit(self.player.hand, self.add_eight, False)  # should be 21
        captured = capsys.readouterr()
        assert self.player.hand.result == Outcome.UNFINISHED
        assert 'Blackjack' in captured.out

    def test_natural_blackjack(self, capsys):
        self.player.hand = Hand(50, [self.ace_of_spades, self.ten_of_clubs])
        self.player.play(self.deck)
        captured = capsys.readouterr()
        assert self.player.hand.result == Outcome.NATURAL
        assert 'natural' in captured.out

    def test_bunch_of_hits(self):
        self.player.hand = Hand(50, [self.three_of_hearts, self.three_of_hearts])
        self.player.hit(self.player.hand, self.add_three, False) #should be 9
        self.player.hit(self.player.hand, self.add_three, False) #should be 12
        self.player.hit(self.player.hand, self.add_three, False) #should be 15
        self.player.hit(self.player.hand, self.add_three, False) #should be 18
        assert self.player.hand.result == Outcome.UNFINISHED
        assert len(self.player.hand) == 6
        self.player.hit(self.player.hand, self.add_eight) #should be 26
        assert self.player.hand.result == Outcome.BUST
        assert len(self.player.hand) == 7

    def test_stand(self, capsys):
        self.player.stand()
        captured = capsys.readouterr()
        assert self.player.hand.result == Outcome.UNFINISHED
        assert len(self.player.hand) == 2
        assert "Standing\n" in captured

    def test_stand_with_more_cards(self):
        self.player.hit(self.player.hand, self.add_three, False)
        self.player.hit(self.player.hand, self.add_three, False)
        self.player.stand()
        assert self.player.hand.result == Outcome.UNFINISHED
        assert len(self.player.hand) == 4

    def test_valid_double(self):
        #self.player.hand = Hand(123, [self.three_of_hearts, self.ten_of_clubs])
        self.player.double(self.player.hand, self.add_three)
        assert self.player.hand.bet == 246
        assert self.player.hand.result == Outcome.UNFINISHED

    def test_invalid_double(self, monkeypatch):
        self.player.hand.set_bet(600) #600 * 2 = 1200 which is more than the 1000 we have.
        monkeypatch.setattr(INPUT, lambda _: "stand")
        self.player.double(self.player.hand, self.add_three) #will fail, then call self.player.play_hand()
        assert self.player.hand.bet == 600 #didn't change to 1200
        assert len(self.player.hand) == 2 #didn't draw a card

    def test_double_bet_edgecase(self):
        self.player.hand.set_bet(500) # * 2 == 1000. Exactly the amount of money we have
        self.player.double(self.player.hand, self.add_three) #should work
        assert self.player.hand.bet == 1000
        assert len(self.player.hand) == 3
        assert self.player.hand.result == Outcome.UNFINISHED

    def test_double_bet_edgecase_plus1(self, monkeypatch):
        self.player.hand.set_bet(501) # * 2 = 1002 which is more than the 1000 we have.
        monkeypatch.setattr(INPUT, lambda _: "stand")
        self.player.double(self.player.hand, self.add_three) #will fail, then call self.player.play_hand()
        assert self.player.hand.bet == 501 #didn't change to 1200
        assert len(self.player.hand) == 2 #didn't draw a card

    def test_valid_surrender(self):
        self.player.surrender(self.player.hand, self.deck)
        assert self.player.hand.result == Outcome.SURRENEDERED

    def test_invalid_surrender_hit(self):
        self.player.hit(self.player.hand, self.add_three, False)
        with patch('Player.Player.play_hand') as play_hand:
            self.player.surrender(self.player.hand, self.deck)
            play_hand.assert_called_once() #assert that surrender returned, then went back to play_hand()

    def test_invalid_split_not_duplicates(self):
        hand = Hand(0, [self.eight_of_diamonds, self.ten_of_clubs])
        with patch('Player.Player.play_hand') as play_hand:
            self.player.split(hand, self.deck)
            play_hand.assert_called_once() #assert that split failed and we went back to play_hand()

    def test_invalid_split_not_enough_money(self):
        hand = Hand(1000, [self.eight_of_diamonds, self.ten_of_clubs]) #player only has $1000
        with patch('Player.Player.play_hand') as play_hand:
            self.player.split(hand, self.deck)
            play_hand.assert_called_once()

    def test_split(self):
        hand = Hand(0, [self.eight_of_diamonds, self.eight_of_diamonds])
        with patch('Player.Player.hit') as hit:
            self.player.split(hand, self.deck)
            assert hit.call_count == 2 #2 hits, one for each split hand
            assert len(self.player.extra_hands) == 1

    def test_3_splits(self):
        hand = Hand(250, [self.eight_of_diamonds, self.eight_of_diamonds])
        self.player.hand = hand
        with patch('Player.Player.hit') as hit:
            self.player.split(hand, self.add_eight)
            self.player.hand.receive_card(self.eight_of_diamonds)
            self.player.split(hand, self.add_eight)
            self.player.hand.receive_card(self.eight_of_diamonds)
            self.player.split(hand, self.add_eight)
            assert hit.call_count == 6 #2 hits per split, one for each split hand
            assert len(self.player.extra_hands) == 3