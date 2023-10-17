import random

class Card(object):
    Rank = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    Suit = ['♥', '♦', '♣', '♠'] 

    def __init__(self, rank, suit): 
        self.rank = rank
        self.suit = suit

    def __str__(self):
        if self.rank == 14: #ถ้าสุ่มได้ rank 14 แสดง A
            rank = 'A'
        elif self.rank == 13: #ถ้าสุ่มได้ rank 13 แสดง K
            rank = 'K'
        elif self.rank == 12: #ถ้าสุ่มได้ rank 12 แสดง Q
            rank = 'Q'
        elif self.rank == 11: #ถ้าสุ่มได้ rank 11 แสดง J
            rank = 'J'
        else:
            rank = self.rank
        return str(rank) + self.suit #other rank แสดงตาม rank นั้น

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
        return self.deck.pop(0) #ไม่มีทางได้ไพ่ซ้ำใบกัน

class BlackjackGame(object):
    def __init__(self):
        self.deck = Deck()

    def calculate_hand_value(self, hand):
        value = 0
        num_aces = 0

        for card in hand:
            rank = card.rank
            if rank in [11, 12, 13]: #J K Q มีค่า 10
                value += 10
            elif rank == 14: # A มีค่า 11
                value += 11
                num_aces += 1
            else:
                value += rank

        # Handle aces ตอนแรก A = 11 แต่ถ้าไพ่ในมือแล้วเกิน 21 A จะกลายเป็น 1
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1

        return value

    def display_player_hand(self, hand):
        print("Your hand: ",end="")
        for card in hand:
            print(str(card), end=" ")
        print()

    def display_dealer_hand(self, hand):
        print("Dealer's hand: ",end="")
        for card in hand:
            print(str(card), end=" ")
        print()

    def display_player_total(self, hand):
        player_value = self.calculate_hand_value(hand)
        print("Your hand value: " + str(player_value))

    def display_dealer_total(self, hand):
        dealer_value = self.calculate_hand_value(hand)
        print("Dealer's total value: " + str(dealer_value))

    def reset_deck(self): #reset ไพ่ให้กลับมาค่าเริ่่มต้น
        self.deck = Deck()

    def play(self):
        while True:
            self.reset_deck() #reset ไพ่ให้กลับมาค่าเริ่่มต้น
            self.deck.shuffle() #สลับไพ่

            player_hand = []
            dealer_hand = []

            # Deal two cards to each player
            player_hand.extend([self.deck.deal(), self.deck.deal()]) #แจกไพ่ 2 ใบ
            dealer_hand.extend([self.deck.deal(), self.deck.deal()]) #แจกไพ่ 2 ใบ

            self.display_dealer_hand([dealer_hand[0]]) #ต้องใช้ [dealer_hand[0]] เพราะว่าใน display_dealer_hand ต้องการ input ที่เป็น list ถึงจะเอาไป run ใน loop ได้ #แสดง dealer's cards แค่ในเดียว
            self.display_player_hand(player_hand)
            self.display_player_total(player_hand)
            player_value = self.calculate_hand_value(player_hand) #ดูค่าไพ่ player

            # Player's turn
            while player_value < 21:
                while True:
                    try:
                        action = input("Do you want to 'hit' or 'stand'? ").strip().lower()
                        if action not in ['hit', 'stand']:
                            raise ValueError("Invalid input. Please enter 'hit' or 'stand'.") # you can use the raise statement to raise a ValueError exception when you encounter an invalid value
                        break 
                    except ValueError as e:
                        print(e)
                if action == "hit":
                    new_card = self.deck.deal()
                    player_hand.append(new_card)
                    print("You drew: " + str(new_card))
                    self.display_player_hand(player_hand)
                    self.display_player_total(player_hand)
                    player_value = self.calculate_hand_value(player_hand)
                elif action == "stand":
                    break

            # Determine the result if the player's value exceeds 21
            if player_value > 21:
                print("Bust! You lose.")

            # Dealer's turn (only if the player didn't bust)
            else:
                while self.calculate_hand_value(dealer_hand) < 17: #The dealer will continue to draw cards until their hand reaches a total value of 17 or higher
                    new_card = self.deck.deal()
                    dealer_hand.append(new_card)

                self.display_dealer_hand(dealer_hand)
                self.display_dealer_total(dealer_hand)
                dealer_value = self.calculate_hand_value(dealer_hand) #ดูค่าไพ่ dealer


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
                            raise ValueError("Invalid input. Please enter 'yes' or 'no'.") # you can use the raise statement to raise a ValueError exception when you encounter an invalid value
                        break
                    except ValueError as e:
                        print(e)
            if play_again == "no":
                break

        print("Thanks for playing Blackjack!")

BlackjackGame().play()

'''
How to grow the win rate
-หยุด ถ้าคุณมี 17 หรือสูงกว่า
-ขอไพ่เสมอถ้าคุณมี 8 หรือน้อยกว่า
-หยุด ถ้าคุณมีระหว่าง 12 และ 16 และเจ้ามือถือระหว่าง 2 และ 6
-ขอไพ่ถ้าคุณมีระหว่าง 12 และ 16 และเจ้ามือถือ A หรือ 7 ขึ้นไป
'''