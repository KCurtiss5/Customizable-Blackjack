import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from Card import Card
from Hand import Hand, Outcome


class TestHand:

    three_of_hearts = Card("Hearts", 3)
    ten_of_clubs = Card("Clubs", 10)
    ace_of_spades = Card("Spades", "Ace")

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.three_card_hand = Hand(
            100, [self.three_of_hearts, self.ten_of_clubs, self.ace_of_spades])

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
            
    def test_constructor_vars(self):
        assert self.three_card_hand.bet == 100
        assert len(self.three_card_hand) == 3
            
    def test_set_bet_with_invalid_bet(self):
        with pytest.raises(ValueError):
            self.three_card_hand.set_bet("bad_int")

    def test_set_bet(self):
        self.three_card_hand.set_bet(50)
        assert self.three_card_hand.bet == 50

    def test_set_bet_zero(self):
        self.three_card_hand.set_bet(0)
        assert self.three_card_hand.bet == 0

    def test_set_result(self):
        self.three_card_hand.set_result(Outcome.UNFINISHED)
        assert self.three_card_hand.result == Outcome.UNFINISHED
        self.three_card_hand.set_result(Outcome.WIN)
        assert self.three_card_hand.result == Outcome.WIN

    def test_clear_hand(self):
        self.three_card_hand.clear_hand()
        assert len(self.three_card_hand) == 0

    def test_take_card(self):
        popped_card = self.three_card_hand.take_card()
        assert popped_card == self.ace_of_spades
        assert len(self.three_card_hand) == 2

    def test_take_card_twice(self):
        self.three_card_hand.take_card()
        self.three_card_hand.take_card()
        assert len(self.three_card_hand) == 1
            
    def test_receive_card_with_invalid_card(self):
        with pytest.raises(ValueError):
            self.three_card_hand.receive_card(0)

    def test_receive_card(self):
        self.three_card_hand.receive_card(self.ten_of_clubs)
        assert len(self.three_card_hand) == 4

    def test_receive_card_twice(self):
        self.three_card_hand.receive_card(self.ten_of_clubs)
        self.three_card_hand.receive_card(self.ace_of_spades)
        assert len(self.three_card_hand) == 5

    def test_get_score_one_ace(self):
        assert self.three_card_hand.get_score() == 14

    def test_get_score_bust(self):
        self.three_card_hand.receive_card(self.ten_of_clubs)
        assert self.three_card_hand.get_score() == 24

    def test_get_score_two_aces(self):
        self.three_card_hand.receive_card(self.ace_of_spades)
        assert self.three_card_hand.get_score() == 15

    def test_get_score_one_ace_gets_to_21(self):
        test_hand = Hand(
            200, [self.ten_of_clubs, self.ace_of_spades])
        assert test_hand.get_score() == 21

    def test_get_score_all_aces(self):
        test_hand = Hand(0, [self.ace_of_spades, self.ace_of_spades, self.ace_of_spades])
        assert test_hand.get_score() == 13

    def test_get_score_regular_cards(self):
        test = Hand(0, [self.ten_of_clubs, self.three_of_hearts])
        assert test.get_score() == 13

    def test_no_card_hand_score(self):
        test = Hand(0, [])
        assert test.get_score() == 0

    def test_judge_hand_win(self):
        self.three_card_hand.judge_hand(10) #14 vs. 10. Win
        assert self.three_card_hand.result == Outcome.WIN

    def test_judge_hand_lose(self):
        self.three_card_hand.judge_hand(17) #14 vs. 17. Lose
        assert self.three_card_hand.result == Outcome.LOSE

    def test_judge_hand_push(self):
        self.three_card_hand.judge_hand(14) #14 vs 14. Push
        assert self.three_card_hand.result == Outcome.PUSH

    def test_judge_hand_edge_case_0(self):
        self.three_card_hand.judge_hand(0)
        assert self.three_card_hand.result == Outcome.WIN

    def test_judge_hand_edge_case_21(self):
        self.three_card_hand.judge_hand(21)
        assert self.three_card_hand.result == Outcome.LOSE

    def test_judge_hand_dealer_bust(self):
        self.three_card_hand.judge_hand(25)
        assert self.three_card_hand.result == Outcome.WIN

    def test_calculate_payout_WIN(self):
        self.three_card_hand.set_result(Outcome.WIN)
        assert self.three_card_hand.calculate_payout() == 100

    def test_calculate_payout_LOSE(self):
        self.three_card_hand.set_result(Outcome.LOSE)
        assert self.three_card_hand.calculate_payout() == -100

    def test_calculate_payout_BUST(self):
        self.three_card_hand.set_result(Outcome.BUST)
        assert self.three_card_hand.calculate_payout() == -100

    def test_calculate_payout_PUSH(self):
        self.three_card_hand.set_result(Outcome.PUSH)
        assert self.three_card_hand.calculate_payout() == 0

    def test_calculate_payout_NATURAL(self):
        self.three_card_hand.set_result(Outcome.NATURAL)
        assert self.three_card_hand.calculate_payout() == 150

    def test_calculate_payout_SURRENDER(self):
        self.three_card_hand.set_result(Outcome.SURRENEDERED)
        assert self.three_card_hand.calculate_payout() == -50

    def test_len_dunder(self):
        assert len(self.three_card_hand) == len(self.three_card_hand.cards)

    def test_getitem_dunder(self):
        assert self.three_card_hand[0] == self.three_of_hearts
        assert self.three_card_hand[1] == self.ten_of_clubs
        assert self.three_card_hand[2] == self.ace_of_spades

    def test_repr_dunder(self):
        assert len(str(self.three_card_hand).split("\n")) == 7
        assert str(self.three_card_hand).count('\u2665') == 3  # 3 hearts
        assert str(self.three_card_hand).count('\u2663') == 10  # 10 clubs
        assert str(self.three_card_hand).count('\u2660') == 1  # and a spade
