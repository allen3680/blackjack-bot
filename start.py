import datetime
import variable
import mysql.connector
import traceback
from time import sleep
from tool import *
from readconfig import *
from my_enum import *
from log_control import *
from action import *

computer_config = readComputerConfig()
bot_w_offset = int(computer_config['w_offset'])
bot_h_offset = int(computer_config['h_offset'])
bot_config = readBotConfig()
bot_no = int(bot_config['no'])
cnx = mysql.connector.connect(**readMysqlConfig())
cursor = cnx.cursor(buffered=True)

def init_play_coordinate():
    command = "select * from play_coordinate where id = %s"
    cursor.execute(command, ('1,1',))
    all_coordinate_result = cursor.fetchall()[0] 
    play_coordinate_dict = dict()
    for i, des in enumerate(cursor.description):
        if bot_no == 1:
            current_w_offset = 0
            current_h_offset = 0
        elif bot_no == 2:
            current_w_offset = bot_w_offset
            current_h_offset = 0
        elif bot_no == 3:
            current_w_offset = 0
            current_h_offset = bot_h_offset
        elif bot_no == 4:
            current_w_offset = bot_w_offset
            current_h_offset = bot_h_offset
        temp_coordinate = all_coordinate_result[i].split(',')
        temp_coordinate[0] = str(int(all_coordinate_result[i].split(',')[0]) + current_w_offset)
        temp_coordinate[1] = str(int(all_coordinate_result[i].split(',')[1]) + current_h_offset)
        result = ','.join(temp_coordinate)
        play_coordinate_dict[des[0]] = result
    return play_coordinate_dict

def play(play_coordinate_dict):
    log_info('play')
    sleep(1)
    get_hand(play_coordinate_dict)
    player = create_player()
    action = filter(player)
    move(play_coordinate_dict, action)
    log_info('play finish')

def main():
    play_coordinate_dict = init_play_coordinate()
    initial()
    is_reshuffle = False
    is_bet = False
    while True:
        try:
            if variable.paused:
                continue
            # 檢查洗牌
            if not is_reshuffle:
                is_reshuffle = check_new_game(play_coordinate_dict)
            # 打牌
            if super_match(play_coordinate_dict, 'confirm_button'):
                card_count_after(is_reshuffle)
                if not is_bet:
                    betsize = get_betsize()
                    place_bet(play_coordinate_dict, betsize)
                    is_bet = True
                sleep(0.3)
                click(play_coordinate_dict, 'confirm_button')
                is_reshuffle = False
            elif super_match(play_coordinate_dict, 'get_card_button'):
                is_bet = False
                play(play_coordinate_dict)
            # 遊戲結束
            elif super_match(play_coordinate_dict, 'dealer_21_label'):
                log_info('dealer_21_label')
                sleep(3.5)
                get_all_hand_img(play_coordinate_dict)
                get_all_hand_value()
                count_win_loss()
                sleep(5)
            elif super_match(play_coordinate_dict, 'player_21_label') & super_rgb_match(play_coordinate_dict, 'player_one_layer_one_card_three') & (super_match(play_coordinate_dict, 'dealer_score_green_label') | super_match(play_coordinate_dict, 'dealer_score_grey_label')):
                log_info('player_21_label')
                sleep(3)
                get_all_hand_img(play_coordinate_dict)
                get_all_hand_value()
                count_win_loss()
                sleep(5)
            elif super_match(play_coordinate_dict, 'dealer_score_orange_label'):
                log_info('dealer_score_orange_label')
                sleep(3)
                get_all_hand_img(play_coordinate_dict)
                get_all_hand_value()
                count_win_loss()
                sleep(5)
            elif super_match(play_coordinate_dict, 'dealer_score_red_label') | super_match(play_coordinate_dict, 'dealer_score_green_label'):
                log_info('dealer_score_red_label')
                sleep(2)
                get_all_hand_img(play_coordinate_dict)
                get_all_hand_value()
                count_win_loss()
                sleep(5)
            elif super_match(play_coordinate_dict, 'player_one_score_red_label') & (super_match(play_coordinate_dict, 'dealer_score_green_label') | super_match(play_coordinate_dict, 'dealer_score_red_label') | super_match(play_coordinate_dict, 'dealer_score_grey_label')):
                log_info('player_one_score_red_label')
                sleep(1)
                get_all_hand_img(play_coordinate_dict)
                get_all_hand_value()
                count_win_loss()
                sleep(5)
            elif super_match(play_coordinate_dict, 'player_one_score_green_label') & (super_match(play_coordinate_dict, 'dealer_score_green_label') | super_match(play_coordinate_dict, 'dealer_score_red_label')):
                log_info('player_one_score_green_label')
                sleep(1)
                get_all_hand_img(play_coordinate_dict)
                get_all_hand_value()
                count_win_loss()
                sleep(5)

            if super_match(play_coordinate_dict, 'dont_buy_insurance_button'):
                decide_to_buy_insurance()
        except Exception:
            log_warning('error:' + traceback.format_exc())
            datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        finally:
            sleep(0.5)



