'''
Created on 3 Aug 2017

@author: qsong
'''
import unittest

from bs4 import BeautifulSoup
import datetime
import json
from selenium import webdriver
import os
import re
import time


class OddInfo(object):
    game_odd_base_url = "http://data.nowgoal.com/3in1odds/{}_{}.html"

    def get_game_odd(self, odd_type, game_id, company_id):
        game_odd_url = self.game_odd_base_url.format(company_id, game_id)
        print(game_odd_url)

        file_dir = os.path.abspath(os.path.dirname(__file__))
        project_dir = file_dir.replace("/src/Odd",'')
        chromedriver_dir = os.path.join(project_dir, "bin/chromedriver")
        print (chromedriver_dir)
        driver = webdriver.Chrome(chromedriver_dir)

        driver.get(game_odd_url)
        time.sleep(10)
        elem = driver.find_element_by_id('main').get_attribute('outerHTML')
        if elem == None:
            return
        day_file = open("../../data/odd/odd_info.html", 'w')
        day_file.write(elem.encode('ascii', 'ignore').decode('ascii'))
        odd_list = self._get_game_odd_from_table()
        if odd_list == None:
            return
        odd_list.reverse()
        print(odd_list)
        self._write_game_odd_info(game_id, company_id, odd_list)
        driver.close()
        day_file.close()
        os.remove("../../data/odd/odd_info.html")
        return

    def _get_game_odd_from_table(self, day_table_file="../../data/odd/odd_info.html"):
        game_odd_list = []
        soup = BeautifulSoup(open(day_table_file), 'html.parser')
        time_odd_table_body = soup.findAll(id='div_l')
        if len(time_odd_table_body) == 0:
            return
        odd_item_list = time_odd_table_body[0].find_all("tr", class_=re.compile(r' gt([1-2])$'))
        print("game has {}".format(len(odd_item_list)))
        for odd_item in odd_item_list:
            odd_item_game_time = odd_item.find_all("td")[0].text  # ingame_time
            odd_item_current_score = odd_item.find_all("td")[1].text  # updated_score
            odd_item_home_rate = odd_item.find_all("td")[2].text  # home_value
            odd_item_odd_type = odd_item.find_all("td")[3].text  # odd_type
            odd_item_away_rate = odd_item.find_all("td")[4].text  # away_value
            odd_item_time = odd_item.find_all("td")[5].text  # updated_time
            odd_item_status = odd_item.find_all("td")[6].text  # odded_status
            # print("odd_item_game_time {} / odd_item_current_score {} / odd_item_home_rate {} / odd_item_odd_type {} / odd_item_away_rate {} /odd_item_away_time {} / odd_item_status {}".format(odd_item_game_time, odd_item_current_score, odd_item_home_rate, odd_item_odd_type, odd_item_away_rate, odd_item_time, odd_item_status))
            odd_dict = {"odd_item_game_time": odd_item_game_time, "odd_item_current_score": odd_item_current_score,
                        "odd_item_home_rate": odd_item_home_rate, "odd_item_odd_type": odd_item_odd_type,
                        "odd_item_away_rate": odd_item_away_rate, "odd_item_time": odd_item_time,
                        "odd_item_status": odd_item_status}
            # print(odd_dict)
            game_odd_list.append(odd_dict)
        return game_odd_list

    def _write_game_odd_info(self, game_id, company_id, odd_list):
        with open("../../data/odd/game{}_company{}_odd.json".format(game_id, company_id), 'w') as odd_file:
            odd_file.write(json.dumps(odd_list))
        return

    def get_yesterday_game_odd(self):
        time_yesterday = datetime.datetime.today() - datetime.timedelta(1)
        time_yesterday = time_yesterday.strftime('%Y-%m-%d')
        self._get_game_odd_per_date(time_yesterday)
        return

    def _get_game_odd_per_date(self, date_str):
        with open("../../data/game/daily_game_info.json", 'r') as data_file:
            data = json.load(data_file)
        game_id_list = data[date_str]
        print(date_str, len(game_id_list))  # date and games number
        if len(game_id_list) < 1:  # in case there is no game by day, or daily is list not in the json
            return
        for game_id in game_id_list:
            self.get_game_odd("handicap", game_id, "3")  # handicap is asian handicap / 3 is the company of SB
            time.sleep(60)
        return


'''
    def get_daily_game_odd(self):
        time_now = datetime.datetime.now()
        time_now = time_now.strftime('%Y-%m-%d')
        self._get_game_odd_per_date(time_now)
        return
'''


class Test(unittest.TestCase):
    def setUp(self):
        self.test_obj = OddInfo()

    def tearDown(self):
        self.test_obj = None
        return

    def test_get_today_game_odd(self):
        # self.test_obj.get_game_odd("handicap", 1554690, "3")
        return

    def test_get_yesterday_game_odd(self):
        self.test_obj.get_yesterday_game_odd()
        return

    def test_get_game_odd(self):
        # self.test_obj.get_game_odd("handicap", "1472351", "3")
        # self.test_obj.get_goldenbet()
        return
