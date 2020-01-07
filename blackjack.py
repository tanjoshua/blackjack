import random

# initialization of the values associated with a standard deck of cards, without the jokers
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

# class for card 
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

# class for deck which comprises of the standard set of cards
class Deck:
    def __init__(self):
        self.deck = []
        for s in suits:
            for r in ranks:
                self.deck.append(Card(s, r))
    
    def __str__(self):
        output = ""
        for card in self.deck:
            output += ("\n" + card.__str__())
        return "The deck contains" + output
    
    def shuffle(self):
        random.shuffle(self.deck)

    # deals the first card from the deck
    def deal(self):
        return self.deck.pop()

# class for the hand of a player/dealer, comprising of the cards dealt to the player/dealer
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    # Aces can be either 1 or 11 points. Thus, the value of the hand should be calculated based on which is more beneficial to the player
    def adjust_for_aces(self):
        while self.value > 21 and self.aces:
            self.aces -= 1
            self.value -= 10

# class for chips, which is used by the player to bet on each round
# Players start with a default 100 chips but can be changed if necessary
class Chips:
    def __init__(self, amount = 100):
        self.amount = amount
        self.bet = 0

    def win_bet(self):
        self.amount += self.bet

    def lose_bet(self):
        self.amount -= self.bet

# function for a player to place a bet for the round
def place_bet(chip):
    while True:
        try:
            chip.bet = int(input("Please place your bet: "))
            if chip.bet <= chip.amount:
                break
            else:
                print("Insufficient funds. Please try again.")
        except:
            print("Invalid input. Please try again.")

# function for player to 'hit', which is drawing a card
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_aces()

# function which asks a player if he wants to hit or stand
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        decision = input("Hit or stand? (Enter H/S): ").upper()
        if decision == "H":
            print("You have chosen to hit")
            hit(deck, hand)
        elif decision == "S":
            print("You have chosen to stand. It is now the dealer's turn.")
            playing = False
        else:
            print("Invalid input. Please enter H (hit) or S (stand).")
            continue

        break
    pass

# function that displays the cards during a game. With the first card of the dealer hidden
def show_game_cards(player, dealer):
    print("The player has: ")
    for card in player.cards:
        print(card)
    print("")

    print("The dealer has: ")
    if dealer.cards:
        print("(Hidden card)")
    for card in dealer.cards[1:]:
        print(card)
    print("")


# function that displays all of the cards at the end of the game. Also shows the value of each hand
def show_all_cards(player, dealer):
    print("The player has:")
    for card in player.cards:
        print(card)
    print("Player's hand has a value of: {}".format(player.value))

    print("The dealer has:")
    for card in dealer.cards:
        print(card)
    print("Dealer's hand has a value of: {}".format(dealer.value))

# The following functions handle the end states of the game
def player_busts(chip):
    print("Player busts! You lose your bet.")
    chip.lose_bet()

def player_wins(chip):
    print("Player wins! You win your bet.")
    chip.win_bet()

def dealer_busts(chip):
    print("Dealer busts! You win your bet.")
    chip.win_bet()
    
def dealer_wins(chip):
    print("Dealer wins! You lose your bet.")
    chip.lose_bet()

def tie():
    print("It's a tie! You keep your bet.")

# play game
def play_game():

    global playing
    # while loop to replay game
    while True:

        # initialize game deck, player and dealer hands, chips
        game_deck = Deck()
        game_deck.shuffle()

        player_hand = Hand()
        dealer_hand = Hand()
        player_chips = Chips()

        # display welcome message and ask player for bet
        print("Welcome to Blackjack! Player starts off with {} chips.".format(player_chips.amount))
        place_bet(player_chips)

        # Deal 2 cards to player and dealer
        print("\n2 Cards are dealt to the player and dealer.")
        player_hand.add_card(game_deck.deal())
        dealer_hand.add_card(game_deck.deal())
        player_hand.add_card(game_deck.deal())
        dealer_hand.add_card(game_deck.deal())
        show_game_cards(player_hand, dealer_hand)

        # Player's turn
        print("Player's turn")
        while playing:
            hit_or_stand(game_deck, player_hand)
            show_game_cards(player_hand, dealer_hand)
            if player_hand.value > 21:
                break

        # if player did not bust, let dealer play
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(game_deck, dealer_hand)
            
        # show all cards and check end scenario
        show_all_cards(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_busts(player_chips)
        elif dealer_hand.value > 21:
            dealer_busts(player_chips)
        elif player_hand.value > dealer_hand.value:
            player_wins(player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        else:
            tie()

        print("Current chip total: {}".format(player_chips.amount))

        # ask to play a new game
        play_again = input("Do you want to play a new game? (Y/N): ").upper()
        if play_again == "Y":
            playing = True
            continue
        else:
            print("Thank you for playing!")
            break

play_game()