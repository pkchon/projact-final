import random

class Card(object):
    Rank = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    Suit = ['♥', '♦', '♣', '♠']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        if self.rank == 14:
            rank = 'A'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 11:
            rank = 'J'
        else:
            rank = self.rank
        return str(rank) + self.suit

class Deck(object):
    def __init__(self):
        self.deck = []
        for suit in Card.Suit:
            for rank in Card.Rank:
                card = Card(rank, suit)
                self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop(0)

class BlackjackGame(object):
    def __init__(self):
        self.deck = Deck()

    def calculate_hand_value(self, hand):
        value = 0
        num_aces = 0

        for card in hand:
            rank = card.rank
            if rank in [11, 12, 13]:
                value += 10
            elif rank == 14:
                value += 11
                num_aces += 1
            else:
                value += rank

        # Handle aces
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1

        return value

    def display_hand(self, hand):
        for card in hand:
            print(str(card), end=" ")

    def display_total(self, hand):
        player_value = self.calculate_hand_value(hand)
        print("Total value: " + str(player_value))

    def reset_deck(self):
        self.deck = Deck()

    def play(self):
        while True:
            self.reset_deck() 
            self.deck.shuffle()

            player_hand = []
            dealer_hand = []

            # Deal two cards to each player
            player_hand.extend([self.deck.deal(), self.deck.deal()])
            dealer_hand.extend([self.deck.deal(), self.deck.deal()])

            print("Your hand: ",end="")
            self.display_hand(player_hand)
            print()
            self.display_total(player_hand)
            player_value = self.calculate_hand_value(player_hand)

            # Player's turn
            while player_value < 21:
                while True:
                    try:
                        action = input("Do you want to 'hit' or 'stand'? ").strip().lower()
                        if action not in ['hit', 'stand']:
                            raise ValueError("Invalid input. Please enter 'hit' or 'stand'.")
                        break 
                    except ValueError as e:
                        print(e)
                if action == "hit":
                    new_card = self.deck.deal()
                    player_hand.append(new_card)
                    print("You drew: " + str(new_card))
                    print("Your hand: ",end="")
                    self.display_hand(player_hand)
                    print()
                    player_value = self.calculate_hand_value(player_hand)
                    print("Total value: " + str(player_value))
                elif action == "stand":
                    break

            # Determine the result if the player's value exceeds 21
            if player_value > 21:
                print("Bust! You lose.")

            # Dealer's turn (only if the player didn't bust)
            if player_value <= 21:
                while self.calculate_hand_value(dealer_hand) < 17: #The dealer will continue to draw cards until their hand reaches a total value of 17 or higher
                    dealer_hand.append(self.deck.deal())

                print("Dealer's hand: ", end="")
                self.display_hand(dealer_hand)
                print()
                dealer_value = self.calculate_hand_value(dealer_hand)
                print("Dealer's total value: " + str(dealer_value))

                # Determine the winner
                if dealer_value > 21:
                    print("Dealer busts! You win.")
                elif player_value > dealer_value:
                    print("You win!")
                elif dealer_value > player_value:
                    print("Dealer wins.")
                else:
                    print("It's a tie!")
            while True:
                    try:
                        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
                        if play_again not in ['yes', 'no']:
                            raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
                        break
                    except ValueError as e:
                        print(e)
            if play_again != "yes":
                break

        print("Thanks for playing Blackjack!")

game = BlackjackGame()
game.play()
