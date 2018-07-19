'''
Created on 3 Aug 2018

@author: qsong
'''
import unittest
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import datetime
import json

class GameInfo(object):
    '''
    This module provides League related function
    '''
    game_base_url = "http://zq.win007.com/analysis/{}.htm"
        
    def __init__(self):
        '''
        Constructor
        '''
        return
    
    def __del__(self):
        return

    def get_daily_game_id(self):
        print("entrance")
        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        driver.get("http://www.nowgoal.com/")
        elem = driver.find_element_by_id('mintable').get_attribute('outerHTML')
        day_file = open("../../data/game/day_table_info.html", 'w+')
        day_file.write(elem.encode('ascii', 'ignore').decode('ascii'))
        day_file.close()
        today_game_list = self._get_game_id_from_day_table()
        self.write_daily_game_info(today_game_list)
        return

    def _get_game_id_from_day_table(self, day_table_file = "../../data/game/day_table_info.html"):
        today_game_list = []
        soup = BeautifulSoup(open(day_table_file),'html.parser')
        onclick = soup.findAll('td', onclick=True)
        for elm in onclick:
            match = re.search(r"showgoallist\(([0-9]+)\)", str(elm))
            today_game_list.append(match.group(1))
        return today_game_list

    def write_daily_game_info(self, game_list):
        time_now = datetime.datetime.now()
        time_now = time_now.strftime('%Y-%m-%d')

        with open("../../data/game/daily_game_info.json", 'r') as data_file:
            data = json.load(data_file)
        print (data)
        data.update({time_now:game_list})

        with open("../../data/game/daily_game_info.json", 'w') as data_file:
            data_file.write(json.dumps(data))

'''
    def get_game_info_by_id (self, game_id):
        game_info_url = self.game_base_url.format(game_id)
        print game_info_url
        opener = urllib2.build_opener()
        headers = {  'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',}
        opener.addheaders = headers.items()
        url_data = opener.open(game_info_url,timeout=10).read()
        soup = BeautifulSoup(url_data)
        odd_table_body = soup.find_all("script")
        print odd_table_body    
        for script_in_body in odd_table_body:
            if script_in_body.text.find("function show_info") != -1 :
                print script_in_body
                game_file = open("../../data/game/game_info"+str(game_id)+".js", 'w+')
                game_file.write(script_in_body.text.encode('ascii', 'ignore').decode('ascii'))
                game_file.close()
        return


        

'''


class Test(unittest.TestCase):

    def setUp(self):
        self.test_obj = GameInfo()

    def tearDown(self):
        self.test_obj = None
        return

    def test_get_game_info(self):
        pass
#         self.test_obj.get_game_info_by_id(1365286)
        # self.test_obj.get_goldenbet()
        return

    def test_get_game_id_per_day(self):
        self.test_obj.get_daily_game_id()
        # self.test_obj.get_goldenbet()
        return


        
        
