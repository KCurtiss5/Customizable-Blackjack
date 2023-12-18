from os import name, system
from pathlib import Path


def validate_int_input(message: str, lower: int, upper: int) -> int:
    while (True):
        try:
            option = int(input(message))
            if ((option < lower) or (option > upper)):
                print(
                    f"Please enter a number between {lower} and {upper}")
                continue
            return (option)
        except ValueError:
            print("Please enter a positive integer.")


def clear_terminal():
    system('cls' if name == 'nt' else 'clear')


def locate_file(file: str) -> str:
    cwd = Path().absolute()
    try:
        path = next(cwd.rglob(file))
    except StopIteration:
        raise RuntimeError(f"Error: {file} not found")
    return path


def get_file_contents(file: str) -> list:
    return open(locate_file(file), "r").read()


def get_card(card) -> str:
    return add_suit(get_file_contents(f"{card.num}.txt"), card)


def get_hand(hand, hidden_card=False, hidden_index=1):
    cards = []
    for index in range(0, len(hand)):
        if (hidden_card and hidden_index == index):
            cards.append(get_file_contents("back.txt"))
        else:
            cards.append(get_card(hand[index]))
    return_string = ""
    for card in zip(*(card.splitlines() for card in tuple(cards))):
        return_string += ' '.join(card) + '\n'
    return return_string


def add_suit(string: str, card) -> str:
    suits = {
        "Spades": '\u2660',
        "Clubs": '\u2663',
        "Diamonds": make_red('\u2666'),
        "Hearts": make_red('\u2665')
    }
    return string.replace('x', suits[card.suit])


def make_red(input: str) -> str:
    return f"\033[91m{input}\033[00m"


def print_banner():
    clear_terminal()
    print(get_file_contents(".banner.txt"))
