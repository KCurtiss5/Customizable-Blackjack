from Card import Card
from Hand import Hand
from abc import ABC, abstractmethod
from helper_functions import get_hand, validate_int_input
from json import JSONEncoder


class Person(ABC):
    @abstractmethod
    def __init__(self):
        self.hand = Hand()

    def add_card_to_hand(self, card: Card):
        self.hand.receive_card(card)


class Dealer(Person):
    def __init__(self, H17=False):
        Person.__init__(self)
        if (not isinstance(H17, bool)):
            raise ValueError(
                f"Error, invalid H17: {H17}.")
        self.H17 = H17  # if true, we hit on 17. Else we stand.

    def should_dealer_hit(self):
        score = self.hand.get_score()
        return self.H17 if score == 17 else score < 17

    def reveal(self):
        return f"Dealer has\n{get_hand(self.hand, True)}"


class Player(Person):
    def __init__(self, name, money):
        Person.__init__(self)
        if not isinstance(name, str):
            raise ValueError(f"Error, invalid name: {name}.")
        self.name = name
        if not isinstance(money, int) and money > 0:
            raise ValueError(f"Error, invalid moneey: {money}.")
        self.money = money
        self.extra_hands = []

    def play(self):
        print(f"\n{self.name} has \n{self.hand}")
        if self.hand.get_score() == 21 and len(self.hand.cards) == 2:
            print(f"{self.name} has natural blackjack!")
            return
        self.play_hand(self.hand)
        for extra_hand in self.extra_hands:
            self.play_hand(extra_hand)
        return
    
    def play_hand(self, hand):
        arg = input(
            f"What do you want to do, {self.name}?: ").lower().strip()
        if (arg == "split"):
            self.split_hand(hand)
        if (arg == 'hit'):
            self.hit(hand, deck)
        elif (arg == "double"):
            self.double(hand)
        elif (arg == 'stand'):
            self.stand(hand)
        else:
            print("Actions are: \"hit\" or \"stand\" or \"double\" or \"split\"")

    def hit(self, hand, deck):
        print("Hit")
        '''self.hand.receiveCard(deck)
                print(f"You drew {str(self.hand.cards[-1])}")
                if (arg == "hit" and self.hand.score < 21):
                    continue
                if (self.hand.score > 21):
                    print("Oops, you busted.")
                if (self.hand.score == 21):
                    print("Blackjack!\n")
        '''

    def stand(self):
        print("Hit")
        '''
        print("Standing.")
                self.hand.setFinished()'''

    def double(self):
        print("Double")
        '''
        if self.hand.bet * 2 > self.money:
                        print(
                            f"{self.name} cannot double down. Not enough money.")
                        continue
                    else:
                        print(
                            f"{self.name} must bet ${self.hand.bet} more.")
                        self.hand.bet *= 2
        '''

    def split_hand(self):
        print("Split")
        '''if (len(player.hand.cards) == 2 and player.hand.cards[0].num == player.hand.cards[1].num
            and len(player.hand) < 3 and player.money-2*player.hand.bet > 0):
            print("Successfully split:\n")
            newHand = Hand(player.hand.bet)
                    transfer_card = player.hand.splitCards(deck)
                    newHand.receiveCard(deck, transfer_card)
                    print(
                        f"You drew a {str(player.hand.cards[-1])} for your first hand.")
                    newHand.receiveCard(deck)
                    print(
                        f"You drew a {str(newHand.cards[-1])} for your second hand.")
                    player.hand.append(newHand)
                    continue'''

    def surrender(self):
        print("Surrender")

    def bet(self, minimum_bet: int):
        self.hand.set_bet(validate_int_input(
            f"{self.name}, place your bet: ", minimum_bet, self.money))

    def __str__(self):
        return (f"{self.name}, you have ${self.money}.")


class PlayerEncoder(JSONEncoder):
    def default(self, obj):
        return {
            "name": obj.name,
            "money": obj.money
        }


if __name__ == "__main__":
    koby = Player("Koby", 1000)
    print(koby)
    koby.bet(50)
    koby.add_card_to_hand(Card("Hearts", 5))
    koby.add_card_to_hand(Card("Clubs", "Ace"))
    koby.play()
