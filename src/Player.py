from json import JSONEncoder
import dataclasses
from abc import ABC, abstractmethod
from Deck import Deck
from Hand import Hand, Outcome
from helper_functions import get_hand, validate_int_input


@dataclasses.dataclass
class Person(ABC):
    @abstractmethod
    def __init__(self):
        self.hand = Hand()


class Dealer(Person):
    def __init__(self, h17=False):
        Person.__init__(self)
        if not isinstance(h17, bool):
            raise ValueError(
                f"Error, invalid H17: {h17}.")
        self.h17 = h17  # if true, we hit on 17. Else we stand.

    def should_dealer_hit(self):
        score = self.hand.get_score()
        return self.h17 if score == 17 else score < 17

    def reveal(self):
        return f"Dealer has\n{get_hand(self.hand, True)}"


class Player(Person):
    def __init__(self, name, money):
        Person.__init__(self)
        if not isinstance(name, str):
            raise ValueError(f"Error, invalid name: {name}.")
        if not isinstance(money, int) or money < 0:
            raise ValueError(f"Error, invalid moneey: {money}.")
        self.name = name
        self.money = money
        self.extra_hands = []

    def bet(self, minimum_bet: int):
        self.hand.set_bet(validate_int_input(
            f"{self.name}, place your bet: ", minimum_bet, self.money))

    def play(self, deck):
        print(f"\n{self.name} has \n{self.hand}")
        if self.hand.get_score() == 21 and len(self.hand.cards) == 2:
            print(f"{self.name} has natural blackjack!")
            self.hand.set_result(Outcome.NATURAL)
            return
        self.play_hand(self.hand, deck)

    def play_hand(self, hand: Hand, deck: Deck):
        arg = input(
            f"What do you want to do, {self.name}?: ").lower().strip()
        if arg == 'hit':
            self.hit(hand, deck)
        elif arg == 'stand':
            self.stand()
        elif arg == "double":
            self.double(hand, deck)
        elif arg == "surrender":
            self.surrender(hand, deck)
        elif arg == "split":
            self.split(hand, deck)
        else:
            print('Use "hit", "stand", "double", "surrender" or "split"')
            self.play_hand(hand, deck)

    def hit(self, hand: Hand, deck: Deck, continue_with_hand=True):
        hand.receive_card(deck.deal_card())
        print(hand)
        if hand.get_score() < 21:
            if continue_with_hand:
                self.play_hand(hand, deck)
            else:
                print(f"Finished with {hand.get_score()}")
        elif hand.get_score() > 21:
            print("Oops, you busted.")
            hand.set_result(Outcome.BUST)
        else:
            print("Blackjack!\n")

    def stand(self):
        print("Standing")

    def double(self, hand, deck):
        if hand.bet * 2 > self.money:
            print("You cannot double down. Not enough money.")
            self.play_hand(hand, deck)
        else:
            print(f"{self.name} must bet ${hand.bet} more.")
            hand.set_bet(hand.bet*2)
            self.hit(hand, deck, False)

    def split(self, hand: Hand, deck: Deck):
        if (len(hand) == 2 and hand[0] == hand[1] and self.money >= 2*hand.bet):
            print("Successfully split\n")
            transfer_card = hand.take_card()
            new_hand = Hand(hand.bet, [transfer_card])
            self.hit(hand, deck)
            self.hit(new_hand, deck)
            self.extra_hands.append(new_hand)
        else:
            print("You can't split.")
            self.play_hand(hand, deck)

    def surrender(self, hand: Hand, deck: Deck):
        if (len(hand) == 2 and len(self.extra_hands) == 0):
            print("Surrendering...")
            hand.set_result(Outcome.SURRENEDERED)
        else:
            print("You can only surrender on your first action.")
            self.play_hand(hand, deck)

    def __str__(self):
        return f"{self.name}, you have ${self.money}."


class PlayerEncoder(JSONEncoder):
    def default(self, o):
        return {
            "name": o.name,
            "money": o.money
        }
