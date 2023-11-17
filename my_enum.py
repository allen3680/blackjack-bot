from enum import Enum

class Action(Enum):
    GetCard = 0
    Stop = 1
    Double = 2
    Split = 3

class Betsize(Enum):
    Left = 'left_button'
    Middle = 'middle_button'
    Right = 'right_button'

card_values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
               'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']

# 定義一個玩家類別
class Player:
    def __init__(self):
        self.hand = []
        self.score = 0
        self.aces = 0
        self.blackjack_or_not = False
        self.double_or_not = False
        self.bust_or_not = False
        self.fiver_little_cards = False

    def add_card(self, card):
        self.hand.append(card)
        self.score += card_values[card]
        if card == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.score > 21 and self.aces:
            self.score -= 10
            self.aces -= 1

    def get_min_score(self):
        min_score =0
        for h in self.hand:
            min_score += card_values[h]
            if h == 'Ace':
                min_score-=10
        return min_score
    
    def check_player_state(self):
        if(self.score == 21 and len(self.hand) == 2):
            self.blackjack_or_not = True
        if(self.score > 21):
            self.bust_or_not = True
        if(self.score <= 21 and len(self.hand) == 5):
            self.fiver_little_cards = True
        return
