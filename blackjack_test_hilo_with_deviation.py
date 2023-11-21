import random
table_info = dict()

# 定義卡片組
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
card_values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
               'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
# 定義一個卡片類別
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

# 定義一個牌堆類別
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]*6
        self.hi_low_count = 0
        self.hi_low_avg = 0
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)
    def deal(self):
        c = self.cards.pop()
        if  card_values[c.rank]>= 2 and  card_values[c.rank] <= 6:
            self.hi_low_count+=1
        elif card_values[c.rank]>= 10 and  card_values[c.rank] <= 11:
            self.hi_low_count-=1
        elif card_values[c.rank]>= 7 and  card_values[c.rank] <= 9:
            self.hi_low_count+=0
        else:
            pass
            # print('878787')
        self.hi_low_avg = self.hi_low_count * 52 / len(self.cards)
        return c

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
        self.split_or_not = False

    def add_card(self, card):
        self.hand.append(card)
        self.score += card_values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.score > 21 and self.aces:
            self.score -= 10
            self.aces -= 1

    def get_min_score(self):
        min_score =0
        for h in self.hand:
            min_score += card_values[h.rank]
            if h.rank == 'Ace':
                min_score-=10
        return min_score
    
# def decide_splitting(player,dealer_card):
#     if card_values[player.hand[0].rank] == 2:
#         if dealer_card >= 2 and dealer_card <= 7:
#             return True
#         else:
#             return False
#     elif card_values[player.hand[0].rank] == 3:
#         if dealer_card >= 2 and dealer_card <= 7:
#             return True
#         else:
#             return False
#     elif card_values[player.hand[0].rank] == 4:
#         if dealer_card >= 5 and dealer_card <= 6:
#             return True
#         else:
#             return False
#     elif card_values[player.hand[0].rank] == 5:
#         return False
#     elif card_values[player.hand[0].rank] == 6:
#         if dealer_card >= 2 and dealer_card <= 6:
#             return True
#         else:
#             return False
#     elif card_values[player.hand[0].rank] == 7:
#         if dealer_card >= 2 and dealer_card <= 7:
#             return True
#         else:
#             return False
#     elif card_values[player.hand[0].rank] == 8:
#         return True
#     elif card_values[player.hand[0].rank] == 9:
#         if dealer_card >= 2 and dealer_card <= 9 and dealer_card != 7:
#             return True
#         else:
#             return False
#     elif card_values[player.hand[0].rank] == 10:
#         return False
#     else:
#         return True
    
# def add_card_or_not(player,dealer_card):
#     print('min',player.get_min_score())
#     if player.get_min_score() <= 11 and (len(player.hand) == 4):
#         return [True,False]
#     elif player.get_min_score() == 3 and player.aces > 0:
#         print('a2')
#         if dealer_card >= 5 and dealer_card <= 6:
#             return [True,True]
#         else:
#             return [True,False]
#     elif player.get_min_score() == 4  and player.aces > 0:
#         print('a3')
#         if dealer_card >= 5 and dealer_card <= 6:
#             return [True,True]
#         else:
#             return [True,False]
#     elif  player.get_min_score() == 5  and player.aces > 0:
#         print('a4')
#         if dealer_card >=4 and dealer_card <= 6:
#             return [True,True]
#         else:
#             return [True,False]
#     elif  player.get_min_score() == 6  and player.aces > 0:
#         print('a5')
#         if dealer_card >=4 and dealer_card <= 6:
#             return [True,True]
#         else:
#             return [True,False]
#     elif  player.get_min_score() == 7  and player.aces > 0:
#         print('a6')
#         if dealer_card >=3 and dealer_card <= 6:
#             return [True,True]
#         else:
#             return [True,False]
#     elif  player.get_min_score() == 8  and player.aces > 0:
#         print('a7')
#         if dealer_card >=3 and dealer_card <= 6:
#             return [True,True]
#         elif dealer_card in [2 ,7,8]:
#             return [False,False]
#         else:
#             return [True,False]
#     elif  player.get_min_score() == 9  and  player.aces > 0:
#         print('a8')
#         return [False,False]
#     elif  player.get_min_score() == 10 and player.aces > 0:
#         print('a9')
#         return [False,False]      
#     elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 2  and player.score == 4):
#         print('22')
#         return [True,False]
#     elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 3  and player.score == 6):
#         print('33')
#         return [True,False]
#     elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 4  and player.score == 8):
#         print('44')
#         return [True,False]
#     elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 6  and player.score == 12):
#         print('66')
#         return [True,False]
#     elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 7  and player.score == 14):
#         print('77')
#         return [True,False]
#     elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 8  and player.score == 16):
#         print('8787878787878787878787878787878')
#         return 1
#     elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 9  and player.score == 18):
#         print('99')
#         return [False,False]
#     elif(player.score >= 5 and player.score <= 8):
#         print('point 8')
#         return [True,False]
#     elif(player.score == 9):
#         print('point 9')
#         if dealer_card >=3 and dealer_card <= 6:
#             return [True,True]
#         else:
#             return [True,False]
#     elif(player.score == 10):
#         print('point 10')
#         if dealer_card >=2 and dealer_card <= 9:
#             return [True,True]
#         else:
#             return [True,False]
#     elif(player.score == 11):
#         print('point 11')
#         if dealer_card >=2 and dealer_card <= 10:
#             return [True,True]
#         else:
#             return [True,False]
#     elif(player.score == 12):
#         print('point 12')
#         if dealer_card >=4 and dealer_card <= 6:
#             return [False,False]
#         else:
#             return [True,False]
#     elif(player.score >= 13 and player.score <=16):
#         print('point 13 - 16')
#         if dealer_card >=2 and dealer_card <= 6:
#             return [False,False]
#         else:
#             return [True,False]
#     elif(player.score >= 17):
#         return [False,False]
#     else:
#         print('unknown error')
#         return 1
    
def decide_splitting(player, dealer_card):
    if card_values[player.hand[0].rank] == 2:
        if dealer_card >= 2 and dealer_card <= 7:
            return True
        else:
            return False
    elif card_values[player.hand[0].rank] == 3:
        if dealer_card >= 2 and dealer_card <= 7:
            return True
        else:
            return False
    elif card_values[player.hand[0].rank] == 4:
        if dealer_card >= 5 and dealer_card <= 6:
            return True
        else:
            return False
    elif card_values[player.hand[0].rank] == 5:
        return False
    elif card_values[player.hand[0].rank] == 6:
        if dealer_card >= 2 and dealer_card <= 6:
            return True
        else:
            return False
    elif card_values[player.hand[0].rank] == 7:
        if dealer_card >= 2 and dealer_card <= 7:
            return True
        else:
            return False
    elif card_values[player.hand[0].rank] == 8:
        return True
    elif card_values[player.hand[0].rank] == 9:
        if dealer_card >= 2 and dealer_card <= 9 and dealer_card != 7:
            return True
        else:
            return False
    elif card_values[player.hand[0].rank] == 10:
        if (dealer_card == 4) & (table_info['true_count'] >= 6):
            return True
        elif (dealer_card == 5) & (table_info['true_count'] >= 5):
            return True
        elif (dealer_card == 6) & (table_info['true_count'] >= 4):
            return True
        else:
            return False
    else:
        return True
    
def add_card_or_not(player, dealer_card):
    # print('dddddddddddd')
    # print(player.hand[0].rank)
    # print('dsfdssdf')
    # print('min', player.get_min_score())
    if player.get_min_score() <= 11 and (len(player.hand) == 4):
        return [True,False]
    elif player.get_min_score() == 3 and player.aces > 0:
        # print('a2')
        if dealer_card >= 5 and dealer_card <= 6:
            return [True,True]
        else:
            return [True,False]
    elif player.get_min_score() == 4  and player.aces > 0:
        # print('a3')
        if dealer_card >= 5 and dealer_card <= 6:
            return [True,True]
        else:
            return [True,False]
    elif  player.get_min_score() == 5  and player.aces > 0:
        # print('a4')
        if dealer_card >=4 and dealer_card <= 6:
            return [True,True]
        else:
            return [True,False]
    elif  player.get_min_score() == 6  and player.aces > 0:
        # print('a5')
        if dealer_card >=4 and dealer_card <= 6:
            return [True,True]
        else:
            return [True,False]
    elif  player.get_min_score() == 7  and player.aces > 0:
        # print('a6')
        if dealer_card >=3 and dealer_card <= 6:
            return [True,True]
        else:
            return [True,False]
    elif  player.get_min_score() == 8  and player.aces > 0:
        # print('a7')
        if dealer_card >= 2 and dealer_card <= 6:
            return [True,True]
        elif dealer_card in [7, 8]:
            return [False,False]
        else:
            return [True,False]
    elif  player.get_min_score() == 9  and  player.aces > 0:
        # print('a8')
        if dealer_card == 6:
            return [True,True]
        elif (dealer_card == 4) & (table_info['true_count'] >= 3):
            return [True,True]
        else:
            return [False,False]
    elif  player.get_min_score() == 10 and player.aces > 0:
        # print('a9')
        return [False,False]      
    elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 2  and player.score == 4):
        # print('22')
        return [True,False]
    elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 3  and player.score == 6):
        # print('33')
        return [True,False]
    elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 4  and player.score == 8):
        # print('44')
        return [True,False]
    elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 6  and player.score == 12):
        # print('66')
        return [True,False]
    elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 7  and player.score == 14):
        # print('77')
        return [True,False]
    elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 8  and player.score == 16):
        # print('8787878787878787878787878787878')
        return 1
    elif (card_values[player.hand[0].rank] == card_values[player.hand[1].rank]) and (card_values[player.hand[0].rank] == 9  and player.score == 18):
        # print('99')
        return [False,False]
    elif(player.score >= 5 and player.score <= 8):
        # print('point 8')
        return [True,False]
    elif(player.score == 9):
        # print('point 9')
        if dealer_card == 2:
            if table_info['true_count'] >= 1:
                return [True,True]
            else:
                return [True,False]
        elif dealer_card == 7:
            if table_info['true_count'] >= 3:
                return [True,True]
            else:
                return [True,False]
        elif dealer_card >=3 and dealer_card <= 6:
            return [True,True]
        else:
            return [True,False]
    elif(player.score == 10):
        # print('point 10')
        if dealer_card >=2 and dealer_card <= 9:
            return [True,True]
        elif dealer_card == 10:
            if table_info['true_count'] >= 4:
                return [True,True]
            else:
                return [True,False]
        elif dealer_card == 11:
            if table_info['true_count'] >= 4:
                return [True,True]
            else:
                return [True,False]
        else:
            return [True,False]
    elif(player.score == 11):
        # print('point 11')
        if dealer_card >=2 and dealer_card <= 10:
            return [True,True]
        elif dealer_card == 11:
            if table_info['true_count'] >= 1:
                return [True,True]
            else:
                return [True,False]
        else:
            return [True,False]
    elif(player.score == 12):
        # print('point 12')
        if dealer_card == 2:
            if table_info['true_count'] >= 3:
                return [False,False]
            else:
                return [True,False]
        elif dealer_card == 3:
            if table_info['true_count'] >= 2:
                return [False,False]
            else:
                return [True,False]
        elif dealer_card == 4:
            if table_info['true_count'] < 0:
                return [True,False]
            else:
                return [False,False]
        elif dealer_card == 5:
            if table_info['true_count'] < -2:
                return [True,False]
            else:
                return [False,False]
        elif dealer_card == 6:
            if table_info['true_count'] < -3:
                return [True,False]
            else:
                return [False,False]
        elif dealer_card >= 5 and dealer_card <= 6:
            return [False,False]
        else:
            return [True,False]
    elif(player.score == 13):
        if (dealer_card == 2):
            if (table_info['true_count'] <= -1):
                return [True,False]
            else:
                return [False,False]
        elif (dealer_card == 3):
            if (table_info['true_count'] <= -2):
                return [True,False]
            else:
                return [False,False]
        elif dealer_card >= 4 and dealer_card <= 6:
            return [False,False]
        else:
            return [True,False]
    elif(player.score == 14):
        # print('point 13 - 16')
        if dealer_card >= 2 and dealer_card <= 6:
            return [False,False]
        else:
            return [True,False]
    elif(player.score == 15):
        # print('point 13 - 16')
        if dealer_card >= 2 and dealer_card <= 6:
            return [False,False]
        elif (dealer_card == 10):
            if (table_info['true_count'] >= 4):
                return [False,False]
            else:
                return [True,False]
        else:
            return [True,False]
    elif(player.score == 16):
        # print('point 13 - 16')
        if dealer_card >= 2 and dealer_card <= 6:
            return [False,False]
        elif (dealer_card == 9):
            if (table_info['true_count'] >= 5):
                return [False,False]
            else:
                return [True,False]
        elif (dealer_card == 10):
            if (table_info['true_count'] >= 0):
                return [False,False]
            else:
                return [True,False]
        else:
            return [True,False]
    elif(player.score >= 17):
        return [False,False]
    else:
        return 1
    
# 定義遊戲流程
def blackjack_game(deck, dealer, default_card, player_list: list):
    # 初始化玩家
    bet = 100
    player = Player()
    player_list.append(player)
    # 發牌給玩家
    if default_card != '':
        player.add_card(default_card)
        player.split_or_not = True
    else:
        player.add_card(deck.deal())
    player.add_card(deck.deal())
    # check player blackjack or not
    if(player.score == 21):
        player.blackjack_or_not = True
    # 決定分不分牌
    split_or_not = False
    if (card_values[player.hand[0].rank] == card_values[player.hand[1].rank] and dealer.blackjack_or_not == False and player.blackjack_or_not == False ):
        split_or_not = decide_splitting(player, card_values[dealer.hand[0].rank])
        if split_or_not:
            player_list.remove(player)
            # print('split!!!!!!!!!!!!')
            blackjack_game(deck, dealer, player.hand[0], player_list)
            blackjack_game(deck, dealer, player.hand[1], player_list)
            return
    player_not_bust = True
    # 如果有人 black jack 就直接下一把
    if (dealer.blackjack_or_not == False and  player.blackjack_or_not == False):
        round = 0
        round_max = 3
        if (player.double_or_not):
            round_max = 1
        # 遊戲迴圈
        while (round <=  round_max) and (player.double_or_not == False):
            # print(f"Your cards: {', '.join(str(card) for card in player.hand)}")
            # print(f"Your score: {player.score}")
            banker_showed_card =  dealer.hand[0]
            # print(f"dealer cards: {banker_showed_card}")

            # 根據表決定是否補牌
            if (player_not_bust):
                decision = add_card_or_not(player,card_values[banker_showed_card.rank])
                draw_card_or_not = decision[0]
                double_or_not = decision[1]
                # 決定何時double
                if round == 0 and double_or_not:
                    player.double_or_not = True
                    if (player.double_or_not):
                        round_max = 1
                        # print('this hand double')
                #choice = input("Do you want to draw another card? (y/n): ").lower()
                if draw_card_or_not :
                    # print('decide to draw hand')
                    player.add_card(deck.deal())
                    player.adjust_for_ace()
                    # 判斷玩家是否爆牌
                    if player.score > 21:
                        player.bust_or_not = True
                    else:
                        player.bust_or_not = False
                else:
                    break
                round+=1
            else:
                break

        if round == 3 and player.score <= 21:
            player.fiver_little_cards = True
    else:
        pass
        # if(dealer.blackjack_or_not):
        #     print('dealer_blackjack')
        # else:
        #     print('player_blackjack')
   
    return

def card_count_after_hilo(player:Player, deck:Deck):
    global table_info
    # Dealer
    for item in player.hand:
        dealer_hand = item.rank
        if dealer_hand in ['Two', 'Three', 'Four', 'Five', 'Six']:
            table_info['count'] += 1
        elif dealer_hand in ['Seven', 'Eight', 'Nine']:
            pass
        elif dealer_hand in ['Ten', 'Jack', 'Queen', 'King', 'Ace']:
            table_info['count'] -= 1
    table_info['true_count'] = table_info['count']/len(deck.cards)*52
    # log_info('count: ' + str(table_info['count']))
    # log_info('true_count: ' + str(table_info['true_count']))
    # log_info('count_for_insurance: ' + str(table_info['count_for_insurance']))
    # log_info('true_count_for_insurance: ' + str(table_info['true_count_for_insurance']))

def get_betsize():
    global table_info
    betsize = 50
    if table_info['true_count'] < 2:
        betsize = 50
    elif (table_info['true_count'] >= 2) & (table_info['true_count'] < 4):
        betsize = 100
    elif (table_info['true_count'] >= 4) & (table_info['true_count'] < 6):
        betsize = 150
    elif (table_info['true_count'] >= 6) & (table_info['true_count'] < 8):
        betsize = 200
    elif (table_info['true_count'] >= 8):
        betsize = 250
    return betsize

# 開始遊戲
def point_count(br, bet, player: Player, dealer: Player, player_win_count, player_lose_count,total_water):
    if player.split_or_not:
        special_card = 1
    else:
        special_card = 1.5
    if player.blackjack_or_not:
        if (dealer.blackjack_or_not):
            Tie = True
        else:
            player_win_count += 1
            br += bet * special_card*0.95
            total_water += bet * special_card*0.05
    if dealer.blackjack_or_not:
        if (player.blackjack_or_not):
            Tie = True
        else:
            player_lose_count += 1
            br -= bet
    if player.double_or_not:
        final_bet = 2*bet
    else:
        final_bet = bet
    # 判斷勝負
    if not dealer.blackjack_or_not and not player.blackjack_or_not:
        if not player.bust_or_not :
            if player.fiver_little_cards:
                if dealer.fiver_little_cards :
                    if player.score < dealer.score:
                        player_win_count += 1
                        br += final_bet * special_card*0.95
                        total_water += final_bet * special_card*0.05
                        # print("Congratulations! You win!, your five litte is smaller than dealer" )
                    else:
                        player_lose_count += 1
                        br -= final_bet
                        # print("Sorry, you lose. dealer five little is smaller than you")
                else:
                    player_win_count += 1
                    br += final_bet * special_card*0.95
                    total_water += final_bet * special_card*0.05
                    # print("Congratulations! You win! you are five little and dealer is not")
            else:
                if dealer.fiver_little_cards:
                    player_lose_count += 1
                    br -= final_bet
                    # print("Sorry, you lose.dealer fiver little and you don't")
                else:
                    if dealer.score > 21 or player.score > dealer.score:
                        player_win_count += 1
                        br += final_bet *0.95
                        total_water += final_bet * 0.05
                        # print("Congratulations! You win!")
                    elif  player.score == dealer.score :
                        Tie = True
                    else:
                        player_lose_count += 1
                        br -= final_bet 
                        # print("Sorry, you lose.")
        else:
            player_lose_count += 1
            br -= final_bet 
            # print("Sorry, you lose.")
    # print('player_lose_count',player_lose_count)
    # print('player_win_count',player_win_count)
    # print('br',round(br, 2))
    # print('total_water',round(total_water*0.89, 2))
    print('win_loss_without_water',round(br + total_water*0.89,2))
    return player_win_count, player_lose_count, br,total_water

def start(player_win_count, player_lose_count, br ,total_water):
    deck = Deck()
    table_info['true_count'] = 0
    table_info['count'] = 0
    while (len(deck.cards) > 156):
        bet = get_betsize()
        # 這邊會不會跟著變動
        player_list = []
        dealer = Player()
        dealer.add_card(deck.deal())
        dealer.add_card(deck.deal())
        if(dealer.score == 21):
            dealer.blackjack_or_not = True
        blackjack_game(deck, dealer, '', player_list)
        all_player_blackjack = True
        someone_not_bust = False
        for player in player_list:
            if not player.blackjack_or_not:
                all_player_blackjack = False
            if not player.bust_or_not:
                someone_not_bust = True
        if (dealer.blackjack_or_not == False and not all_player_blackjack):
            # 莊家的回合
            # 莊家繼續要牌，直到達到最低分數
            dealer_add_card_count = 0
            while (dealer.score < 17) and (dealer_add_card_count < 3) and someone_not_bust:
                dealer.add_card(deck.deal())
                dealer_add_card_count += 1
                dealer.adjust_for_ace()
                if dealer.score > 21:
                    dealer.bust_or_not = True
            if (dealer_add_card_count == 3) and (dealer.score <= 21):
                dealer.fiver_little_cards = True
        # 計分
        # print('player_list:', player_list)
        # if len(player_list) >= 3:
            # print('three split')
        for player in player_list:
            # print(f"Your cards: {', '.join(str(card) for card in player.hand)}")
            # print(f"\nYour final score: {player.score}")
            # print(f"Dealer's cards: {', '.join(str(card) for card in dealer.hand)}")
            # print(f"Dealer's score: {dealer.score}")
            player_win_count, player_lose_count, br,total_water = point_count(br, bet, player, dealer, player_win_count, player_lose_count,total_water)
        for player in player_list+[dealer]:
            card_count_after_hilo(player, deck)

        # win_count = player_win_count - old_win_count
        # lose_count = player_lose_count - old_lose_count
        # if (current_hi_low > 0) & (current_hi_low < 1):
        #     win_count = hi_low_table['0-1'][0] + win_count
        #     lose_count = hi_low_table['0-1'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['0-1'][3] + 1
        #     else:
        #         bust_count = hi_low_table['0-1'][3]
        #     hi_low_table['0-1'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif (current_hi_low >= 1) & (current_hi_low < 2):
        #     win_count = hi_low_table['1-2'][0] + win_count
        #     lose_count = hi_low_table['1-2'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['1-2'][3] + 1
        #     else:
        #         bust_count = hi_low_table['1-2'][3]
        #     hi_low_table['1-2'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif (current_hi_low >= 2) & (current_hi_low < 3):
        #     win_count = hi_low_table['2-3'][0] + win_count
        #     lose_count = hi_low_table['2-3'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['2-3'][3] + 1
        #     else:
        #         bust_count = hi_low_table['2-3'][3]
        #     hi_low_table['2-3'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif (current_hi_low >= 3) & (current_hi_low < 4):
        #     win_count = hi_low_table['3-4'][0] + win_count
        #     lose_count = hi_low_table['3-4'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['3-4'][3] + 1
        #     else:
        #         bust_count = hi_low_table['3-4'][3]
        #     hi_low_table['3-4'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif (current_hi_low >= 4) & (current_hi_low < 5):
        #     win_count = hi_low_table['4-5'][0] + win_count
        #     lose_count = hi_low_table['4-5'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['4-5'][3] + 1
        #     else:
        #         bust_count = hi_low_table['4-5'][3]
        #     hi_low_table['4-5'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif current_hi_low >= 5:
        #     win_count = hi_low_table['5'][0] + win_count
        #     lose_count = hi_low_table['5'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['5'][3] + 1
        #     else:
        #         bust_count = hi_low_table['5'][3]
        #     hi_low_table['5'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif (current_hi_low > -1) & (current_hi_low < 0):
        #     win_count = hi_low_table['-1'][0] + win_count
        #     lose_count = hi_low_table['-1'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['-1'][3] + 1
        #     else:
        #         bust_count = hi_low_table['-1'][3]
        #     hi_low_table['-1'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif (current_hi_low > -2) & (current_hi_low <= -1):
        #     win_count = hi_low_table['-2'][0] + win_count
        #     lose_count = hi_low_table['-2'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['-2'][3] + 1
        #     else:
        #         bust_count = hi_low_table['-2'][3]
        #     hi_low_table['-2'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif (current_hi_low > -3) & (current_hi_low <= -2):
        #     win_count = hi_low_table['-3'][0] + win_count
        #     lose_count = hi_low_table['-3'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['-3'][3] + 1
        #     else:
        #         bust_count = hi_low_table['-3'][3]
        #     hi_low_table['-3'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif (current_hi_low > -4) & (current_hi_low <= -3):
        #     win_count = hi_low_table['-4'][0] + win_count
        #     lose_count = hi_low_table['-4'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['-4'][3] + 1
        #     else:
        #         bust_count = hi_low_table['-4'][3]
        #     hi_low_table['-4'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif (current_hi_low > -5) & (current_hi_low <= -4):
        #     win_count = hi_low_table['-5'][0] + win_count
        #     lose_count = hi_low_table['-5'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['-5'][3] + 1
        #     else:
        #         bust_count = hi_low_table['-5'][3]
        #     hi_low_table['-5'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif current_hi_low <= -5:
        #     win_count = hi_low_table['-6'][0] + win_count
        #     lose_count = hi_low_table['-6'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['-6'][3] + 1
        #     else:
        #         bust_count = hi_low_table['-6'][3]
        #     hi_low_table['-6'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # elif current_hi_low == 0:
        #     win_count = hi_low_table['0'][0] + win_count
        #     lose_count = hi_low_table['0'][1] + lose_count
        #     win_rate = win_count/(win_count+lose_count)
        #     if dealer.bust_or_not:
        #         bust_count = hi_low_table['0'][3] + 1
        #     else:
        #         bust_count = hi_low_table['0'][3]
        #     hi_low_table['0'] = [win_count, lose_count, win_rate, bust_count, bust_count/(win_count+lose_count)]
        # print('left card num', len(deck.cards))
    return player_win_count, player_lose_count, br,total_water
count = 0
player_win_count = 0
player_lose_count = 0
br = 0
total_water = 0
# hi_low_table = dict()
# hi_low_table['0-1'] = [0, 1, 0, 0, 0]
# hi_low_table['1-2'] = [0, 1, 0, 0, 0]
# hi_low_table['2-3'] = [0, 1, 0, 0, 0]
# hi_low_table['3-4'] = [0, 1, 0, 0, 0]
# hi_low_table['4-5'] = [0, 1, 0, 0, 0]
# hi_low_table['5'] = [0, 1, 0, 0, 0]
# hi_low_table['-1'] = [0, 1, 0, 0, 0]
# hi_low_table['-2'] = [0, 1, 0, 0, 0]
# hi_low_table['-3'] = [0, 1, 0, 0, 0]
# hi_low_table['-4'] = [0, 1, 0, 0, 0]
# hi_low_table['-5'] = [0, 1, 0, 0, 0]
# hi_low_table['-6'] = [0, 1, 0, 0, 0]
# hi_low_table['0'] = [0, 1 ,0, 0, 0]
while count <= 160000:
    player_win_count, player_lose_count, br,total_water = start(player_win_count, player_lose_count, br,total_water)
    count += 1


# print(hi_low_table)