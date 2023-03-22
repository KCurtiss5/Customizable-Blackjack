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


def locate_file(fileName: str) -> str:
    cwd = Path().absolute()
    if str(cwd.parents[0]).endswith("blackjack"):
        cwd = cwd.parents[0]
    try:
        path = next(cwd.rglob(fileName))
    except StopIteration:
        raise RuntimeError("File not found")
    return path


def returnFile(fileName: str) -> list:
    return open(locate_file(fileName), "r").readlines()


def get_card(card) -> str:
    string = "\n"
    for line in returnFile(f"{card.num}.txt"):
        line = add_suit(line, card)
        string += line
    return string


def get_hand(Hand, hidden_card=False, hidden_card_index=-1) -> str:
    files = []
    for index in range(0, len(Hand)):
        if (hidden_card and hidden_card_index == index):
            files.append(open(locate_file("back.txt"), 'r'))
        else:
            files.append(open(locate_file(f"{Hand[index].num}.txt"), 'r'))
    string = ""
    for i in range(0, 6):
        for j in range(len(Hand.cards)):
            additional_line = files[j].readline().rstrip()
            additional_line = add_suit(additional_line, Hand.cards[j])
            string += additional_line
            if i == 0:  # super weird thing about character spacing
                string += ' '
        string += '\n'
    return string


def add_suit(string: str, card) -> str:
    suits = {
        "Spades": '\u2660',
        "Clubs": '\u2663',
        "Diamonds": prRed('\u2666'),
        "Hearts": prRed('\u2665')
    }
    return string.replace('x', suits[card.suit])


def prRed(input: str) -> str:
    return f"\033[91m{input}\033[00m"


def printBanner():
    clear_terminal()
    for line in returnFile(".banner.txt"):
        print(line, end="")
