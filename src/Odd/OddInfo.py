'''
Created on 3 Aug 2017

@author: qsong
'''
import unittest
import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
import json
from selenium import webdriver
import os


class OddInfo(object):
    game_odd_base_url = "http://data.nowgoal.com/3in1odds/{}_{}.html"

    def get_game_odd(self, odd_type, game_id, company_id):
        game_odd_url = self.game_odd_base_url.format(company_id, game_id)
        print(game_odd_url)
        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        driver.get(game_odd_url)
        elem = driver.find_element_by_id('main').get_attribute('outerHTML')
        day_file = open("../../data/odd/odd_info.html", 'w+')
        day_file.write(elem.encode('ascii', 'ignore').decode('ascii'))
        day_file.close()
        os.remove("../../data/odd/odd_info.html")
        return

    def get_yesterday_game_odd(self):
        time_yesterday = datetime.datetime.today() - datetime.timedelta(1)
        time_yesterday = time_yesterday.strftime('%Y-%m-%d')
        self._get_game_odd_per_date(time_yesterday)
        return

    def get_daily_game_odd(self):
        time_now = datetime.datetime.now()
        time_now = time_now.strftime('%Y-%m-%d')
        self._get_game_odd_per_date(time_now)
        return

    def _get_game_odd_per_date(self, date_str):
        with open("../../../data/game/daily_game_info.json", 'r') as data_file:
            data = json.load(data_file)
        game_id_list = data[date_str]
        print  (date_str, len(game_id_list))  # date and games number
        if len(game_id_list) < 1:  # in case there is no game by day, or daily is list not in the json
            return
        for game_id in game_id_list:
            self.get_game_odd("handicap", game_id, "3")  # handicap is asian handicap / 3 is the company of SB

        return


class Test(unittest.TestCase):
    def setUp(self):
        self.test_obj = OddInfo()

    def tearDown(self):
        self.test_obj = None
        return

    def test_get_today_game_odd(self):
        self.test_obj.get_game_odd("handicap", 1553811, "3")
        return

    #     def test_download_season_league_all(self):
    #         league_id_list = self.test_obj.league_id_list
    #         season_list = self.test_obj.season_list
    #         self.test_obj.download_season_league_all(league_id_list, season_list)
    #         return True

    def test_get_game_odd(self):
        # self.test_obj.get_game_odd("handicap", "1472351", "3")
        # self.test_obj.get_goldenbet()
        return

