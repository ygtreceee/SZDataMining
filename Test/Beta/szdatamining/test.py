import io
import json

import pandas as pd
import requests
from tabulate import tabulate
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import matplotlib.pyplot as plt
import base64
from requests.exceptions import JSONDecodeError
import time
from selenium import webdriver

class mySpider:
    def __init__(self):
        self.ask_url = "http://zjj.sz.gov.cn:8004/api/marketInfoShow/getFjzsInfoData"

    def getData(self, dateType="", startDate="", endDate=""):
        # 爬取数据
        ask_params = {
            "dateType": dateType,
            "endDate": endDate,
            "startDate": startDate,
        }
        resp = requests.post(self.ask_url, json=ask_params)
        data = resp.json()['data']
        return data

    @staticmethod
    def get_accumulation(data):
        return [sum(data["ysfTotalTs"]),
                sum(data["esfTotalTs"]),
                sum(data["ysfDealArea"]),
                sum(data["esfDealArea"])]


    def getWeeks(self):
        weekday, today_date = datetime.datetime.now().weekday(), datetime.datetime.now().date()
        monday = today_date - datetime.timedelta(days=weekday)
        date = [[monday - datetime.timedelta(days=i*7), monday - datetime.timedelta(days=i*7-6)] for i in range(1, 4)]
        period = [i[0].strftime("%Y.%m.%d")[5:] + "-" + i[1].strftime("%Y.%m.%d")[5:] for i in date]
        period.insert(0, monday.strftime("%Y.%m.%d")[5:] + "-" + today_date.strftime("%Y.%m.%d")[5:])
        print(period)

        date = [[i[0].strftime("%Y-%m-%d"), i[1].strftime("%Y-%m-%d")] for i in date]
        data = [self.getData(startDate=s, endDate=e) for s, e in date]
        data.insert(0, self.getData(startDate=monday.strftime("%Y-%m-%d"), endDate=today_date.strftime("%Y-%m-%d")))
        [print(item) for item in data]
        data_acc = [self.get_accumulation(item) for item in data]
        value = [item[1] for item in data_acc]
        print(value)
        content = {
            "getWeeks": [
                period,
                value,
            ]
        }
        return content

    def get_totweeks(self):
        Monday = datetime.date(2023, 1, 2)
        Sunday = Monday + datetime.timedelta(days=6)
        today_date = datetime.datetime.now().date()
        date = []
        data = []
        while Sunday < today_date:
            date.append([Monday, Sunday])
            data.append(self.getData(startDate=Monday.strftime("%Y-%m-%d"), endDate=(Sunday.strftime("%Y-%m-%d"))))
            print(Monday, Sunday)
            Monday = Monday + datetime.timedelta(days=7)
            Sunday = Monday + datetime.timedelta(days=6)
        [print(item1, item2) for item1, item2 in zip(date, data)]
        # print(date)
        # print(data)

    def test(self):
        # driver = webdriver.Edge()
        # driver.get("http://zjj.sz.gov.cn/ris/szfdc/showcjgs/esfcjgs.aspx")
        # time.sleep(1000)
        resp = requests.post("http://zjj.sz.gov.cn/ris/szfdc/showcjgs/esfcjgs.aspx")
        # data = resp.json()['data']
        # print(data)
        print(resp.text)

if __name__ == "__main__":
    spiderman = mySpider()
    # spiderman.upload_data()
    # spiderman.timer()
    spiderman.test()