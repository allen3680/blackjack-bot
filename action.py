import nums_from_string as nfs
from mysql.connector.cursor import MySQLCursor
from tool import screenshot, ocr_basic
from my_enum import *
from tool import *
from time import sleep
import re
import datetime
import uuid
import math
from itertools import *
from log_control import *
table_info = dict()

def initial():
    global table_info
    table_info['count'] = 0
    table_info['true_count'] = 0
    table_info['count_for_insurance'] = 0
    table_info['true_count_for_insurance'] = 0
    table_info['remain_card'] = 312
    table_info['dealer_layer'] = 0
    table_info['middle_win_count'] = 0
    table_info['middle_lose_count'] = 0
    table_info['right_win_count'] = 0
    table_info['right_lose_count'] = 0
    for hand in ['one', 'two', 'three', 'four', 'five']:
        table_info['dealer_hand_' + hand] = ''
        for player in ['one', 'two', 'three', 'four']:
            table_info['player_' + player + '_hand_' + hand] = ''
    for player in ['one', 'two', 'three', 'four']:
        table_info['player_' + player + '_layer'] = ''
        for layer in ['one', 'two', 'three', 'four']:
            table_info['player_' + player + '_layer_' + layer + '_card'] = 0
            table_info['player_' + player + '_layer_' + layer + '_is_double'] = False
            for hand in ['one', 'two', 'three', 'four', 'five']:
                table_info['player_' + player + '_layer_' + layer + '_hand_' + hand] = ''

def create_player():
    global table_info
    new_player = Player()
    for player in ['one']:
        for hand in ['one', 'two', 'three', 'four', 'five']:
            if table_info['player_' + player + '_hand_' + hand] in ranks:
                new_player.add_card(table_info['player_' + player + '_hand_' + hand])
    new_player.adjust_for_ace()
    return new_player

def get_hand(coordinate_dict):
    global table_info
    layer_convert = {'one': 'two', 'two': 'three', 'three': 'four', 'four': ''}
    card_convert = {'three': 2, 'four': 3, 'five': 4}
    offset_convert = {'one': 0, 'two': -41, 'three': -82, 'four': -123}
    hand_num_list = ['one', 'two', 'three', 'four', 'five']
    # Dealer
    for hand in ['one', 'two', 'three', 'four', 'five']:
        table_info['dealer_hand_' + hand] = ''
    table_info['dealer_hand_one'] = card_transfer(super_ocr(coordinate_dict, 'dealer_hand_one', 'basic'))
    log_info('進行中 dealer_hand_one: ' + str(table_info['dealer_hand_one']))
    # Player
    for player in ['one']:
        # 初始化
        table_info['player_' + player + '_layer'] = ''
        for layer in ['one', 'two', 'three', 'four']:
            table_info['player_' + player + '_layer_' + layer + '_card'] = 0
            table_info['player_' + player + '_layer_' + layer + '_is_double'] = False
        for hand in ['one', 'two', 'three', 'four', 'five']:
            table_info['player_' + player + '_hand_' + hand] = ''
        # 判斷層數
        is_layer_match = False
        for layer in ['one', 'two', 'three', 'four']:
            if (layer == 'four') & (not is_layer_match):
                table_info['player_' + player + '_layer'] = layer
                break
            else:
                if super_rgb_match(coordinate_dict, 'player_' + player + '_layer_' + layer_convert[layer] + '_card_one_1') | super_rgb_match(coordinate_dict, 'player_' + player + '_layer_' + layer_convert[layer] + '_card_one_2') | super_rgb_match(coordinate_dict, 'player_' + player + '_layer_' + layer_convert[layer] + '_card_one_3') | super_rgb_match(coordinate_dict, 'player_' + player + '_layer_' + layer_convert[layer] + '_card_one_4'):
                    is_layer_match = True
                    table_info['player_' + player + '_layer'] = layer
                    break
        # 判斷牌數
        layer_now = table_info['player_' + player + '_layer']
        is_card_match = False
        for card in ['three', 'four']:
            if super_rgb_match(coordinate_dict, 'player_' + player + '_layer_' + layer_now + '_card_' + card):
                is_card_match = True
                table_info['player_' + player + '_layer_' + layer_now + '_card'] = card_convert[card]
                break
        if not is_card_match:
            table_info['player_' + player + '_layer_' + layer_now + '_card'] = 4
        log_info('進行中 player: ' + player + '的層數: ' + str(table_info['player_' + player + '_layer']) + ', 牌數: ' + str(table_info['player_' + player + '_layer_' + layer_now + '_card']))
        # 截圖辨識牌面
        for i in range(table_info['player_' + player + '_layer_' + layer_now + '_card']):
            screenshot(coordinate_dict['player_' + player + '_hand_' + hand_num_list[i]].split(',')[0], int(coordinate_dict['player_' + player + '_hand_' + hand_num_list[i]].split(',')[1]) + offset_convert[layer_now], coordinate_dict['player_' + player + '_hand_' + hand_num_list[i]].split(',')[2], coordinate_dict['player_' + player + '_hand_' + hand_num_list[i]].split(',')[3], './screenshot/player_' + player + '_hand_' + hand_num_list[i] + '_new.png')
            table_info['player_' + player + '_hand_' + hand_num_list[i]] = card_transfer(ocr_basic('./screenshot/player_' + player + '_hand_' + hand_num_list[i] + '_new.png'))
            log_info('進行中 player_' + player + '_hand_' + hand_num_list[i] + ': ' + str(table_info['player_' + player + '_hand_' + hand_num_list[i]]))
    return

def get_all_hand_img(coordinate_dict):
    global table_info
    layer_convert = {'one': 'two', 'two': 'three', 'three': 'four', 'four': ''}
    card_convert = {'three': 2, 'four': 3, 'five': 4}
    offset_convert = {'one': 0, 'two': -41, 'three': -82, 'four': -123}
    hand_num_list = ['one', 'two', 'three', 'four', 'five']
    # 初始化
    for player in ['one', 'two', 'three', 'four']:
        table_info['player_' + player + '_layer'] = ''
        for layer in ['one', 'two', 'three', 'four']:
            table_info['player_' + player + '_layer_' + layer + '_card'] = 0
            table_info['player_' + player + '_layer_' + layer + '_is_double'] = False
    # Dealer
    is_card_match = False
    for card in ['three', 'four', 'five']:
        if super_rgb_match(coordinate_dict, 'dealer_card_' + card):
            is_card_match = True
            table_info['dealer_layer'] = card_convert[card]
            break
    if not is_card_match:
        table_info['dealer_layer'] = 5
    for i in range(table_info['dealer_layer']):
        screenshot(coordinate_dict['dealer_hand_' + hand_num_list[i]].split(',')[0], coordinate_dict['dealer_hand_' + hand_num_list[i]].split(',')[1], coordinate_dict['dealer_hand_' + hand_num_list[i]].split(',')[2], coordinate_dict['dealer_hand_' + hand_num_list[i]].split(',')[3], './screenshot/dealer_hand_' + hand_num_list[i] + '_new.png')
    log_info('結束後 Dealer牌數: ' + str(table_info['dealer_layer']))
    # Player
    for player in ['one', 'two', 'three', 'four']:
        if not super_match(coordinate_dict, 'player_' + player + '_place_bet_label'):
            continue
        # 判斷層數
        is_layer_match = False
        for layer in ['one', 'two', 'three', 'four']:
            if (layer == 'four') & (not is_layer_match):
                table_info['player_' + player + '_layer'] = layer
                break
            else:
                if super_rgb_match(coordinate_dict, 'player_' + player + '_layer_' + layer_convert[layer] + '_card_one_1') | super_rgb_match(coordinate_dict, 'player_' + player + '_layer_' + layer_convert[layer] + '_card_one_2') | super_rgb_match(coordinate_dict, 'player_' + player + '_layer_' + layer_convert[layer] + '_card_one_3') | super_rgb_match(coordinate_dict, 'player_' + player + '_layer_' + layer_convert[layer] + '_card_one_4'):
                    is_layer_match = True
                    table_info['player_' + player + '_layer'] = layer
                    break
        # 判斷牌數
        for layer in ['one', 'two', 'three', 'four']:
            is_card_match = False
            for card in ['three', 'four', 'five']:
                if super_rgb_match(coordinate_dict, 'player_' + player + '_layer_' + layer + '_card_' + card):
                    is_card_match = True
                    table_info['player_' + player + '_layer_' + layer + '_card'] = card_convert[card]
                    break
            if not is_card_match:
                table_info['player_' + player + '_layer_' + layer + '_card'] = 5
            if layer == table_info['player_' + player + '_layer']:
                break
        log_info('結束後 player: ' + player + '的層數: ' + str(table_info['player_' + player + '_layer']) + ', 牌數: ' + str(table_info['player_' + player + '_layer_' + layer + '_card']))
        # 截圖
        for layer in ['one', 'two', 'three', 'four']:
            # Double
            if super_match(coordinate_dict, 'player_' + player + '_layer_' + layer + '_double_label'):
                table_info['player_' + player + '_layer_' + layer + '_is_double'] = True
                table_info['player_' + player + '_layer_' + layer + '_card'] = 2
                screenshot(coordinate_dict['player_' + player + '_layer_' + layer + '_double_card'].split(',')[0], coordinate_dict['player_' + player + '_layer_' + layer + '_double_card'].split(',')[1], coordinate_dict['player_' + player + '_layer_' + layer + '_double_card'].split(',')[2], coordinate_dict['player_' + player + '_layer_' + layer + '_double_card'].split(',')[3], './screenshot/player_' + player + '_layer_' + layer + '_double_card_new.png')
            # Other
            for i in range(table_info['player_' + player + '_layer_' + layer + '_card']):
                screenshot(coordinate_dict['player_' + player + '_hand_' + hand_num_list[i]].split(',')[0], int(coordinate_dict['player_' + player + '_hand_' + hand_num_list[i]].split(',')[1]) + offset_convert[layer], coordinate_dict['player_' + player + '_hand_' + hand_num_list[i]].split(',')[2], coordinate_dict['player_' + player + '_hand_' + hand_num_list[i]].split(',')[3], './screenshot/player_' + player + '_layer_' + layer + '_hand_' + hand_num_list[i] + '_new.png')
            if layer == table_info['player_' + player + '_layer']:
                break
    return

def get_all_hand_value(coordinate_dict):
    global table_info
    hand_num_list = ['one', 'two', 'three', 'four', 'five']
    # 初始化
    for hand in ['one', 'two', 'three', 'four', 'five']:
        table_info['dealer_hand_' + hand] = ''
    for player in ['one', 'two', 'three', 'four']:
        for layer in ['one', 'two', 'three', 'four']:
            for hand in ['one', 'two', 'three', 'four', 'five']:
                table_info['player_' + player + '_layer_' + layer + '_hand_' + hand] = ''
    # Dealer
    log_info('Dealer')
    for i in range(table_info['dealer_layer']):
        table_info['dealer_hand_' + hand_num_list[i]] = card_transfer(ocr_basic('./screenshot/dealer_hand_' + hand_num_list[i] + '_new.png'))
        log_info('結束後 dealer_hand_' + hand_num_list[i] + ': ' + str(table_info['dealer_hand_' + hand_num_list[i]]))
    # Player
    for player in ['one', 'two', 'three', 'four']:
        if not super_match(coordinate_dict, 'player_' + player + '_place_bet_label'):
            continue
        log_info('Player ' + player)
        # 辨識牌面
        for layer in ['one', 'two', 'three', 'four']:
            # Other
            for i in range(table_info['player_' + player + '_layer_' + layer + '_card']):
                table_info['player_' + player + '_layer_' + layer + '_hand_' + hand_num_list[i]] = card_transfer(ocr_basic('./screenshot/player_' + player + '_layer_' + layer + '_hand_' + hand_num_list[i] + '_new.png'))
                log_info('結束後 player_' + player + '_layer_' + layer + '_hand_' + hand_num_list[i] + ': ' + str(table_info['player_' + player + '_layer_' + layer + '_hand_' + hand_num_list[i]]))
            # Double
            if table_info['player_' + player + '_layer_' + layer + '_is_double']:
                table_info['player_' + player + '_layer_' + layer + '_hand_three'] = card_transfer(ocr_basic_rotate('./screenshot/player_' + player + '_layer_' + layer + '_double_card_new.png'))
                log_info('結束後 player_' + player + '_layer_' + layer + '_hand_three: ' + str(table_info['player_' + player + '_layer_' + layer + '_hand_three']))
            if layer == table_info['player_' + player + '_layer']:
                break
    return

def decide_splitting(player, dealer_card):
    if card_values[player.hand[0]] == 2:
        if dealer_card >= 2 and dealer_card <= 7:
            return True
        else:
            return False
    elif card_values[player.hand[0]] == 3:
        if dealer_card >= 2 and dealer_card <= 7:
            return True
        else:
            return False
    elif card_values[player.hand[0]] == 4:
        if dealer_card >= 5 and dealer_card <= 6:
            return True
        else:
            return False
    elif card_values[player.hand[0]] == 5:
        return False
    elif card_values[player.hand[0]] == 6:
        if dealer_card >= 2 and dealer_card <= 6:
            return True
        else:
            return False
    elif card_values[player.hand[0]] == 7:
        if dealer_card >= 2 and dealer_card <= 7:
            return True
        else:
            return False
    elif card_values[player.hand[0]] == 8:
        return True
    elif card_values[player.hand[0]] == 9:
        if dealer_card >= 2 and dealer_card <= 9 and dealer_card != 7:
            return True
        else:
            return False
    elif card_values[player.hand[0]] == 10:
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
    elif (card_values[player.hand[0]] == card_values[player.hand[1]]) and (card_values[player.hand[0]] == 2  and player.score == 4):
        # print('22')
        return [True,False]
    elif (card_values[player.hand[0]] == card_values[player.hand[1]]) and (card_values[player.hand[0]] == 3  and player.score == 6):
        # print('33')
        return [True,False]
    elif (card_values[player.hand[0]] == card_values[player.hand[1]]) and (card_values[player.hand[0]] == 4  and player.score == 8):
        # print('44')
        return [True,False]
    elif (card_values[player.hand[0]] == card_values[player.hand[1]]) and (card_values[player.hand[0]] == 6  and player.score == 12):
        # print('66')
        return [True,False]
    elif (card_values[player.hand[0]] == card_values[player.hand[1]]) and (card_values[player.hand[0]] == 7  and player.score == 14):
        # print('77')
        return [True,False]
    elif (card_values[player.hand[0]] == card_values[player.hand[1]]) and (card_values[player.hand[0]] == 8  and player.score == 16):
        # print('8787878787878787878787878787878')
        return 1
    elif (card_values[player.hand[0]] == card_values[player.hand[1]]) and (card_values[player.hand[0]] == 9  and player.score == 18):
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
        log_info('Unknown error !!!!!!')
        return 1
    
def decide_to_buy_insurance(coordinate_dict):
    global table_info
    click(coordinate_dict, 'dont_buy_insurance_button')
    # if table_info['true_count_for_insurance'] >= 4:
    #     click(coordinate_dict, 'buy_insurance_button')
    # else:
    #     click(coordinate_dict, 'dont_buy_insurance_button')

def filter(player:Player):
    global table_info
    banker_showed_card = table_info['dealer_hand_one']
    action = Action.Stop
    # 決定分不分牌
    if (card_values[player.hand[0]] == card_values[player.hand[1]]):
        if decide_splitting(player, card_values[banker_showed_card]):
            action = Action.Split
            return action
    # 根據表決定是否補牌
    [draw_card_or_not, double_or_not] = add_card_or_not(player,card_values[banker_showed_card])
    # 決定何時double
    if (len(player.hand) == 2) and double_or_not:
        action = Action.Double
    elif draw_card_or_not:
        action = Action.GetCard
    else:
        action = Action.Stop
    return action

def card_count_after_wonghalf(is_reshuffle):
    global table_info
    if is_reshuffle:
        return
    # Dealer
    for item in ['dealer_hand_one', 'dealer_hand_two', 'dealer_hand_three', 'dealer_hand_four', 'dealer_hand_five']:
        dealer_hand = table_info[item]
        if dealer_hand != '':
            table_info['remain_card'] -= 1
        if dealer_hand == 'Five':
            table_info['count'] += 1.5
        elif dealer_hand in ['Three', 'Four', 'Six']:
            table_info['count'] += 1
        elif dealer_hand in ['Two', 'Seven']:
            table_info['count'] += 0.5
        elif dealer_hand == 'Eight':
            pass
        elif dealer_hand == 'Nine':
            table_info['count'] -= 0.5
        elif dealer_hand in ['Ten', 'Jack', 'Queen', 'King', 'Ace']:
            table_info['count'] -= 1

        if dealer_hand in ['Four', 'Five']:
            table_info['count_for_insurance'] += 2
        elif dealer_hand in ['Two', 'Three', 'Six', 'Seven']:
            table_info['count_for_insurance'] += 1
        elif dealer_hand in ['Eight', 'Nine', 'Ace']:
            pass
        elif dealer_hand in ['Ten', 'Jack', 'Queen', 'King']:
            table_info['count_for_insurance'] -= 2
    # Player
    for player in ['one', 'two', 'three', 'four']:
        for layer in ['one', 'two', 'three', 'four']:
            for hand in ['one', 'two', 'three', 'four', 'five']:
                player_hand = table_info['player_' + player + '_layer_' + layer + '_hand_' + hand]
                if player_hand != '':
                    table_info['remain_card'] -= 1
                if player_hand == 'Five':
                    table_info['count'] += 1.5
                elif player_hand in ['Three', 'Four', 'Six']:
                    table_info['count'] += 1
                elif player_hand in ['Two', 'Seven']:
                    table_info['count'] += 0.5
                elif player_hand == 'Eight':
                    pass
                elif player_hand == 'Nine':
                    table_info['count'] -= 0.5
                elif player_hand in ['Ten', 'Eleven', 'Queen', 'King', 'Ace']:
                    table_info['count'] -= 1
                if dealer_hand in ['Four', 'Five']:
                    table_info['count_for_insurance'] += 2
                elif dealer_hand in ['Two', 'Three', 'Six', 'Seven']:
                    table_info['count_for_insurance'] += 1
                elif dealer_hand in ['Eight', 'Nine', 'Ace']:
                    pass
                elif dealer_hand in ['Ten', 'Eleven', 'Queen', 'King']:
                    table_info['count_for_insurance'] -= 2
    table_info['true_count'] = table_info['count']/(table_info['remain_card']/52)
    table_info['true_count_for_insurance'] = table_info['count_for_insurance']/(table_info['remain_card']/52)
    log_info('count: ' + str(table_info['count']))
    log_info('true_count: ' + str(table_info['true_count']))
    log_info('count_for_insurance: ' + str(table_info['count_for_insurance']))
    log_info('true_count_for_insurance: ' + str(table_info['true_count_for_insurance']))

def card_count_after_hilo(is_reshuffle):
    global table_info
    if is_reshuffle:
        return
    # Dealer
    for item in ['dealer_hand_one', 'dealer_hand_two', 'dealer_hand_three', 'dealer_hand_four', 'dealer_hand_five']:
        dealer_hand = table_info[item]
        if dealer_hand != '':
            table_info['remain_card'] -= 1
        if dealer_hand in ['Two', 'Three', 'Four', 'Five', 'Six']:
            table_info['count'] += 1
        elif dealer_hand in ['Seven', 'Eight', 'Nine']:
            pass
        elif dealer_hand in ['Ten', 'Jack', 'Queen', 'King', 'Ace']:
            table_info['count'] -= 1

        if dealer_hand in ['Four', 'Five']:
            table_info['count_for_insurance'] += 2
        elif dealer_hand in ['Two', 'Three', 'Six', 'Seven']:
            table_info['count_for_insurance'] += 1
        elif dealer_hand in ['Eight', 'Nine', 'Ace']:
            pass
        elif dealer_hand in ['Ten', 'Jack', 'Queen', 'King']:
            table_info['count_for_insurance'] -= 2
    # Player
    for player in ['one', 'two', 'three', 'four']:
        for layer in ['one', 'two', 'three', 'four']:
            for hand in ['one', 'two', 'three', 'four', 'five']:
                player_hand = table_info['player_' + player + '_layer_' + layer + '_hand_' + hand]
                if player_hand != '':
                    table_info['remain_card'] -= 1
                if player_hand in ['Two', 'Three', 'Four', 'Five', 'Six']:
                    table_info['count'] += 1
                elif player_hand in ['Seven', 'Eight', 'Nine']:
                    pass
                elif player_hand in ['Ten', 'Jack', 'Queen', 'King', 'Ace']:
                    table_info['count'] -= 1

                if dealer_hand in ['Four', 'Five']:
                    table_info['count_for_insurance'] += 2
                elif dealer_hand in ['Two', 'Three', 'Six', 'Seven']:
                    table_info['count_for_insurance'] += 1
                elif dealer_hand in ['Eight', 'Nine', 'Ace']:
                    pass
                elif dealer_hand in ['Ten', 'Eleven', 'Queen', 'King']:
                    table_info['count_for_insurance'] -= 2
    table_info['true_count'] = table_info['count']/(table_info['remain_card']/52)
    table_info['true_count_for_insurance'] = table_info['count_for_insurance']/(table_info['remain_card']/52)
    log_info('count: ' + str(table_info['count']))
    log_info('true_count: ' + str(table_info['true_count']))
    log_info('count_for_insurance: ' + str(table_info['count_for_insurance']))
    log_info('true_count_for_insurance: ' + str(table_info['true_count_for_insurance']))


def get_betsize():
    global table_info
    betsize = [Betsize.Left, 1]
    table_info['bet_middle'] = False
    table_info['bet_right'] = False
    if table_info['true_count'] < 1.5:
        betsize = [Betsize.Left, 1]
    elif (table_info['true_count'] >= 1.5) & (table_info['true_count'] < 4):
        betsize = [Betsize.Middle, 1]
        table_info['bet_middle'] = True
    elif (table_info['true_count'] >= 4) & (table_info['true_count'] < 6):
        betsize = [Betsize.Right, 1]
        table_info['bet_middle'] = True
    elif (table_info['true_count'] >= 6) & (table_info['true_count'] < 8):
        betsize = [Betsize.Middle, 2]
        table_info['bet_right'] = True
    elif (table_info['true_count'] >= 8):
        betsize = [Betsize.Left, 5]
        table_info['bet_right'] = True
    return betsize

def place_bet(coordinate_dict, betsize):
    for i in range(betsize[1]):
        click(coordinate_dict, betsize[0].value)
        sleep(0.3)

def check_new_game(coordinate_dict):
    global table_info
    if super_match(coordinate_dict, 'reshuffle_label') | super_match(coordinate_dict, 'full_deck_label'):
        log_info('reshuffle!!!!!!!!!!!!')
        table_info['count'] = 0
        table_info['true_count'] = 0
        table_info['count_for_insurance'] = 0
        table_info['true_count_for_insurance'] = 0
        table_info['remain_card'] = 312
        return True
    return False

def move(coordinate_dict, action):
    log_info('action: ' + str(action))
    if action == Action.GetCard:
        click(coordinate_dict, 'get_card_button')
        sleep(2)
    elif action == Action.Double:
        click(coordinate_dict, 'double_button')
    elif action == Action.Split:
        click(coordinate_dict, 'split_button')
        sleep(2)
    elif action == Action.Stop:
        click(coordinate_dict, 'stop_button')

def card_transfer(card):
    if card == 'A':
        return 'Ace'
    elif card == '2':
        return 'Two'
    elif card in ['3', '3)']:
        return 'Three'
    elif card == '4':
        return 'Four'
    elif card in ['‘5', '5']:
        return 'Five'
    elif card in ['6', '6.']:
        return 'Six'
    elif card in ['7', '7.']:
        return 'Seven'
    elif card == '8':
        return 'Eight'
    elif card in ['fe)', '9', 'Ad']:
        return 'Nine'
    elif card in ['10', '0','lO']:
        return 'Ten'
    elif card == 'J':
        return 'Jack'
    elif card in ['Q', 'e]']:
        return 'Queen'
    elif card == 'K':
        return 'King'
    elif card == '':
        return ''
    else:
        log_info('unknown card!!!!!! card: ' + str(card))
        return ''

def count_win_loss():
    if (not table_info['bet_right']) & (not table_info['bet_middle']):
        log_info('right_win_count: ' + str(table_info['right_win_count']))
        log_info('right_lose_count: ' + str(table_info['right_lose_count']))
        log_info('middle_win_count: ' + str(table_info['middle_win_count']))
        log_info('middle_lose_count: ' + str(table_info['middle_lose_count']))
        return
    if table_info['bet_right']:
        betsize = 'right'
    else:
        betsize = 'middle'
    # create player list
    player_list = []
    int(str(table_info['player_one_layer'])[0]) == 2
    for i in range(1, int(str(table_info['player_one_layer'])[0])+1):
        if i == 1:
            layer = 'one'
        elif i == 2:
            layer = 'two'
        elif i == 3:
            layer = 'three'
        elif i == 4:
            layer = 'four'
        player = Player()
        # for j in range(1, int(str(table_info['player_one_layer'])[1]) + 2):
        for j in range(1, 6):
            if j == 1:
                hand = 'one'
            elif j == 2:
                hand = 'two'
            elif j == 3:
                hand = 'three'
            elif j == 4:
                hand = 'four'
            elif j == 5:
                hand = 'five'
            if table_info['player_one_layer_' + layer + '_hand_' + hand] != '':
                player.add_card(table_info['player_one_layer_' + layer + '_hand_' + hand])
        player.adjust_for_ace()
        player.check_player_state()
        player_list.append(player)
    # create dealer
    dealer = Player()
    for j in range(1, table_info['dealer_layer'] + 2):
        if j == 1:
            hand = 'one'
        elif j == 2:
            hand = 'two'
        elif j == 3:
            hand = 'three'
        elif j == 4:
            hand = 'four'
        elif j == 5:
            hand = 'five'
        if table_info['dealer_hand_' + hand] != '':
            dealer.add_card(table_info['dealer_hand_' + hand])
        dealer.adjust_for_ace()
        dealer.check_player_state()
    win_count = table_info[betsize + '_win_count']
    lose_count = table_info[betsize + '_lose_count']
    for player in player_list:
        win_count, lose_count = point_count(player, dealer, win_count, lose_count)
    table_info[betsize + '_win_count'] = win_count
    table_info[betsize + '_lose_count'] = lose_count
    log_info('right_win_count: ' + str(table_info['right_win_count']))
    log_info('right_lose_count: ' + str(table_info['right_lose_count']))
    log_info('middle_win_count: ' + str(table_info['middle_win_count']))
    log_info('middle_lose_count: ' + str(table_info['middle_lose_count']))
    return 

def point_count(player: Player, dealer: Player, player_win_count, player_lose_count):
    win_lose_base = 1
    if player.blackjack_or_not:
        if (dealer.blackjack_or_not):
            Tie = True
        else:
            player_win_count += win_lose_base
    if dealer.blackjack_or_not:
        if (player.blackjack_or_not):
            Tie = True
        else:
            player_lose_count += win_lose_base
    if player.double_or_not:
        win_lose_base = 2*win_lose_base
    else:
        win_lose_base = win_lose_base
    # 判斷勝負
    if not dealer.blackjack_or_not and not player.blackjack_or_not:
        if not player.bust_or_not :
            if player.fiver_little_cards:
                if dealer.fiver_little_cards :
                    if player.score < dealer.score:
                        player_win_count += win_lose_base
                    else:
                        player_lose_count += win_lose_base
                else:
                    player_win_count += win_lose_base
            else:
                if dealer.fiver_little_cards:
                    player_lose_count += win_lose_base
                else:
                    if dealer.score > 21 or player.score > dealer.score:
                        player_win_count += win_lose_base
                    elif  player.score == dealer.score :
                        Tie = True
                    else:
                        player_lose_count += win_lose_base
        else:
            player_lose_count += win_lose_base
    return player_win_count, player_lose_count
