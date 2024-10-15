from cgitb import handler
from enum import Enum
import random
import os

class CardSuit(Enum):
    CUORI = 0
    QUADRI = 1
    FIORI = 2
    PICCHE = 3

class CardValue(Enum):
    ASSO = 1
    DUE = 2
    TRE = 3
    QUATTRO = 4
    CINQUE = 5
    SEI = 6
    SETTE = 7
    OTTO = 8
    NOVE = 9
    DIECI = 10
    JACK = "J"
    DONNA = "Q"
    RE = "K"

class Card:
    def __init__(self, value: CardValue, suit: CardSuit):
        self.value = value
        self.suit = suit
        self.suits = "♥♦♣♠"

    def __str__(self):
        return (f"{self.value.value}{self.suits[self.suit.value]}")

class Deck:
    def __init__(self):
        self.cards: list[Card] = []
        self.discards: list[Card] = []

    def __str__(self):
        cards = []
        for card in self.cards:
            cards.append(card.__str__())

        return str(cards)
    
    # Deck Functions
    # ==============
    # Creates a standard deck
    def build(self):
        self.cards.clear()
        for i in range(2):
            for suit in CardSuit:
                for value in CardValue:
                    self.add_card(Card(value, suit))
        
    # Shuffles the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Returns the number of cards of the deck
    @property
    def count(self):
        return len(self.cards)

    # Cards Functions
    # ===============
    # Adds a card to the deck
    def add_card(self, card: Card):
        self.cards.append(card)
    
    # Adds a cards to the discard deck
    def add_cards_to_discards(self, cards: list[Card]):
        self.discards += cards 
    
    # Draws n cards from the deck
    def draws_card(self, count: int):
        cards = []
        for i in range(count):
            if(self.count == 0):
                self.cards = self.discards.copy()
                self.shuffle()
                self.discards = []

            cards.append(self.cards.pop(0))

        return cards

class Player:
    def __init__(self, budget: int = 0, hand: list[Card] = []):
        self.budget = budget
        self.hand = []

    def __str__(self):
        cards = []
        for card in self.hand:
            cards.append(card.__str__())

        return str(cards)
    
    # Adds a list of cards to the hand
    def add_cards(self, cards: list[Card]):
        self.hand += cards

    def clear_hand(self):
        self.hand = []

    
    # Returns the total value of the player hand
    @property
    def total(self):
        total = self.total_no_aces()

        aces_count = 0
        for card in self.hand:
            value = card.value.value
            if value == 1:
                aces_count += 1

        if aces_count > 0:
            if aces_count == 1:
                if total + 11 <= 21:
                    total += 11
                    return total
                else:
                    total += 1
                    return total
            else:
                partial = total
                for i in range(aces_count):
                    partial += 1
                
                if partial >= 21:
                    return partial
                elif partial < 21:
                    while (partial - 1) + 11 < 21:
                        partial += 10 # 11 - 1
                    
                    return partial
                
        return total
    
    def total_no_aces(self):
        total = 0
        for card in self.hand:
            value = card.value.value
            if value == "J" or value == "Q" or value == "K":
                value = 10

            if value != 1:
                total += value

        return total

    @property
    def can_double(self):
        if len(self.hand) > 2:
            return False
        return True
    
    @property
    def can_split(self):
        if not self.can_double():
            return False
        
        if Card(self.hand[0]).value.value != Card(self.hand[1]).value.value:
            return False
        
        return True

def clear():
    os.system("cls")

def print_centered(length, string, new_line = True):
    if new_line:
        print(" " * ((length - len(string)) // 2) + string)
    else:
        print(" " * ((length - len(string)) // 2) + string, end="")

def print_space():
    print("\n==================================================\n")

def print_hands():
    clear()
    print_space()
    
    print_centered(50, f"Mano Giocatore: {player} ({player.total})")
    print_centered(50, f"Mano Dealer: [{dealer.hand[0]}]")

def reveal_hands():
    clear()
    print_space()
    
    print_centered(50, f"Mano Giocatore: {player} ({player.total})")
    print_centered(50, f"Mano Dealer: {dealer} ({dealer.total})")



deck = Deck()
deck.build()
deck.shuffle()

print_space()
print_centered(50, "Inserisci il tuo BUDGET INIZIALE: ", False)
starting_budget = float(input("$"))
print_space()

player = Player(starting_budget)
dealer = Player()

while True:
    if player.budget <= 0:
        break

    bet = 0
    while bet == 0 or bet > player.budget:
        print_centered(50, f"Hai ${player.budget}. Quanto vuoi scommettere? ", False)
        bet = float(input("$"))
        print_space()
    
    deck.add_cards_to_discards(player.hand)
    deck.add_cards_to_discards(dealer.hand)

    player.clear_hand()
    dealer.clear_hand()

    deck.shuffle()

    print(player.total, dealer.total)
    player.add_cards(deck.draws_card(2))
    dealer.add_cards(deck.draws_card(2))

    if (player.total == 21 and dealer.total == 21):
        reveal_hands()
        print_space()
        print_centered(50, "DOPPIO BLACKJACK!")
        print_centered(50, "PAREGGIO!")
        print_space()
        continue
    elif (player.total == 21):
        reveal_hands()
        print_space()
        print_centered(50, "HAI BLACKJACK!")
        print_centered(50, "HAI VINTO!")
        print_space()
        player.budget += bet * 1.5  
        continue
    elif (dealer.total == 21):
        reveal_hands()
        print_space()
        print_centered(50, "IL BANCO HA BLACKJACK!")
        print_centered(50, "HAI PERSO!")
        print_space()
        player.budget -= bet  
        continue

    stop = False
    while not stop:
        print_hands()

        print_space()
        print("Cosa vuoi fare?")
        print(" [0] Stop")
        print(" [1] Carta")
        if(player.can_double): print(" [2] Raddoppio")
        if(player.can_split): print(" [2] Raddoppio")
    
        choice = input("> ")

        if choice == "0":
            stop = True
        elif choice == "1":
            player.add_cards(deck.draws_card(1))
            print_hands()

            if(player.total > 21):
                stop = True
        elif choice == "2" and player.can_double:
            player.add_cards(deck.draws_card(1))
            print_hands()
            
            stop = True
        elif choice == "3" and player.can_double:
            print("Can Double")
        else:
            continue
        

    reveal_hands()
    if player.total > 21:
        print_space()
        print_centered(50, "HAI SBALLATO!")
        print_centered(50, "HAI PERSO!")
        print_space()
        player.budget -= bet
    else:
        if dealer.total > player.total:
            print_space()
            print_centered(50, "HAI PERSO!")
            print_space()
            player.budget -= bet
        elif dealer.total == player.total:
            print_space()
            print_centered(50, "PAREGGIO!")
            print_space()
        else:
            if dealer.total > 16:
                print_space()
                print_centered(50, "HAI VINTO!")
                print_space()
                player.budget += bet
            else:
                while dealer.total < 17:
                    dealer.add_cards(deck.draws_card(1))

                reveal_hands()

                if dealer.total > 21:
                    print_space()
                    print_centered(50, "IL BANCO HA SBALLATO!")
                    print_centered(50, "HAI VINTO!")
                    print_space()
                    player.budget += bet
                else:
                    if dealer.total > player.total:
                        print_space()
                        print_centered(50, "HAI PERSO!")
                        print_space()
                        player.budget -= bet
                    elif dealer.total == player.total:
                        print_space()
                        print_centered(50, "Pareggio!")
                        print_space()
                    else:
                        print_space()
                        print_centered(50, "HAI VINTO!")
                        print_space()
                        player.budget += bet
                

print_centered(50, "SEI AL VERDE!")
print_centered(50, "HAI PERSO TUTTO!")
print_space()
