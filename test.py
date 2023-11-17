import datetime
import variable
import mysql.connector
import traceback
from find_table import find_table, detect_empty_table, check_firsttime, find_club
from time import sleep
from action import *
from tool import *
from readconfig import *
from redis_tool import *
from my_enum import *
from situation_control import check_everything
from log_control import *
from find_table import *

computer_config = readComputerConfig()
bot_offset = int(computer_config['offset'])
computer_team = computer_config['team']

bot_config = readBotConfig()
bot_no = int(bot_config['no'])
bot_bigblind = bot_config['bigblind']
bot_club = bot_config['club']
bot_club_count = int(bot_config['club_count'])
bot_club_list = bot_config['club_list'].split(',')

cnx = mysql.connector.connect(**readMysqlConfig())
cursor = cnx.cursor(buffered=True)
table_info = dict()
def check_aab_board():
    global table_info
    public_card_0 = '13s'
    public_card_1 = '13c'
    public_card_2 = '5d'
    public_card_0_num = nfs.get_nums(public_card_0)[0]
    public_card_1_num = nfs.get_nums(public_card_1)[0]
    public_card_2_num = nfs.get_nums(public_card_2)[0]
    if public_card_0_num == 1:
        public_card_0_num = 14
    if public_card_1_num == 1:
        public_card_1_num = 14
    if public_card_2_num == 1:
        public_card_2_num = 14
    card_num_list = [public_card_0_num, public_card_1_num, public_card_2_num]
    card_num_list.sort(reverse=True)

    duplicated_card_num = 0
    duplicated_count = 0
    for i in range(len(card_num_list) - 1):
        for j in range(i + 1, len(card_num_list)):
            if (card_num_list[i] == card_num_list[j]):
                duplicated_card_num = card_num_list[i]
                duplicated_count += 1

    if duplicated_count >= 1:
        print('card_num_list:',card_num_list)
        card_num_list.remove(duplicated_card_num)
        card_num_list.remove(duplicated_card_num)
        print('card_num_list:',card_num_list)
        print(duplicated_card_num, card_num_list[0])
        if (duplicated_card_num - card_num_list[0]) > 0:
            print('1')
            table_info['a_bigger_than_b'] = 'True'
        else:
            print('2')
            table_info['a_bigger_than_b'] = 'False'
        return True
    else:
        table_info['a_bigger_than_b'] = ''
        return False
    
check_aab_board()