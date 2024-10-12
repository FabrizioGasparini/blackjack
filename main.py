from enum import Enum
import random

class CardSuit(Enum):
    CUORI = 0
    QUADRI = 1
    FIORI = 2
    PICCHE = 3

class CardValue(Enum):
    UNO = 1
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
    def add_card_to_discards(self, card: Card):
        self.discards.append(card) 
    
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

    
    # Returns the total value of the player hand
    @property
    def total(self):
        total = 0
        for card in self.hand:
            value = card.value.value
            if value == "J" or value == "Q" or value == "K":
                value = 10

            total += value

        return total

deck = Deck()
deck.build()
deck.shuffle()

starting_budget = int(input("Inserisci il tuo BUDGET INIZIALE: "))
player = Player(starting_budget)

dealer = Player()

while True:
    bet = 0
    while bet == 0 or bet > player.budget:
        bet = int(input(f"Hai ${player.budget}. Quanto vuoi scommettere? "))
    
    deck.shuffle()

    player.add_cards(deck.draws_card(2))
    dealer.add_cards(deck.draws_card(2))

    print(f"Mano Giocatore: {player} ({player.total})")
    print(f"Mano Dealer: [{dealer.hand[0]}]")


# ♥♦♣♠
