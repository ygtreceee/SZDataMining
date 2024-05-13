import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import time
import calendar
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

class mySpider:
    def __init__(self):
        self.ask_url = "http://zjj.sz.gov.cn:8004/api/marketInfoShow/getFjzsInfoData"

    # 根据给定日期获取成交数据
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

    # 对数据进行累加
    @staticmethod
    def get_accumulation(data):
        return [sum(data["ysfTotalTs"]),
                sum(data["esfTotalTs"]),
                sum(data["ysfDealArea"]),
                sum(data["esfDealArea"])]

    # 获取本月成交数据
    def get_lastMonth(self):
        print("get_lastMonth...")
        current_date = datetime.datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        yesterday = current_date - datetime.timedelta(days=1)
        startDate = f"{yesterday.year}-{yesterday.month}-01"
        endDate = f"{yesterday.year}-{yesterday.month}-{yesterday.day}"
        data = self.getData(startDate=startDate, endDate=endDate)
        # print(startDate, endDate)
        # print(data)
        val = self.get_accumulation(data)
        content = {
            "yesterdayYsf": data['ysfTotalTs'][-1],
            "lastMonthYsf":  val[0],
            "yesterdayEsf": data['esfTotalTs'][-1],
            "lastMonthEsf": val[1],
        }
        print(content)
        return content

    # 获取三个月为周期的成交环比
    def get_transactionRatio(self):
        print("get_transactionRatio...")
        current_date = datetime.datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        data = []
        period = [""]
        ratio = []
        for i in range(1, 6):
            beforeThreeMonth = month - 3
            beforeYear = year
            if beforeThreeMonth <= 0:
                beforeThreeMonth += 12
                beforeYear -= 1
            startDate = f"{beforeYear}-{str(beforeThreeMonth).zfill(2)}-{day}"
            endDate = f"{year}-{str(month).zfill(2)}-{day}"
            # print(startDate, endDate)
            # print(self.getData(startDate=startDate, endDate=endDate))
            data.append(self.get_accumulation(self.getData(startDate=startDate, endDate=endDate)))
            month, year = beforeThreeMonth, beforeYear
            if i > 1:
                ratio.append(f"{round((data[0][1] / data[i - 1][1] - 1) * 100)}")
            startDate = startDate[:4] + '.' + startDate[5:7]
            endDate = endDate[:4] + '.' + endDate[5:7]
            if i == 1:
                ratio.append(startDate[2:7] + '-' + endDate[2:7])
            else:
                period.append(startDate[2:7] + '-' + endDate[2:7])
        content = {
            "transactionRatio": [
                period,
                ratio,
            ]
        }
        print(content)
        return content

    # 获取三个月为周期的成交量绝对值
    def get_threeMonthCycle(self):
        print("get_threeMonthCycle...")
        current_date = datetime.datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        period = []
        value = []
        for i in range(1, 6):
            beforeThreeMonth = month - 3
            beforeYear = year
            if beforeThreeMonth <= 0:
                beforeThreeMonth += 12
                beforeYear -= 1
            startDate = f"{beforeYear}-{str(beforeThreeMonth).zfill(2)}-{day}"
            endDate = f"{year}-{str(month).zfill(2)}-{day}"
            # print(startDate, endDate)
            # print(self.getData(startDate=startDate, endDate=endDate))
            data = self.getData(startDate=startDate, endDate=endDate)
            # print(data)
            data = self.get_accumulation(data)

            month, year = beforeThreeMonth, beforeYear

            startDate = startDate[2:4] + '.' + startDate[5:7]
            endDate = endDate[2:4] + '.' + endDate[5:7]
            # print(data)
            # print(startDate, endDate)
            value.append(data[1])
            period.append(startDate + "-" + endDate)

        # print(period)
        # print(value)
        content = {
            # 二手房近三月成交套数
            "numberSecondhandHouseSoldRecentThreeMonth": [
                period,
                value,
            ]
        }
        print(content)
        return content

    # 得到近四周的成交量绝对值
    def getWeeks(self):
        print("getWeeks...")
        last_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
        weekday = last_date.weekday()
        monday = last_date - datetime.timedelta(days=weekday)
        date = [[monday - datetime.timedelta(days=i*7), monday - datetime.timedelta(days=i*7-6)] for i in range(1, 4)]
        period = [i[0].strftime("%Y.%m.%d")[5:] + "-" + i[1].strftime("%Y.%m.%d")[5:] for i in date]
        period.insert(0, monday.strftime("%Y.%m.%d")[5:] + "-" + last_date.strftime("%Y.%m.%d")[5:])
        # print(period)

        date = [[i[0].strftime("%Y-%m-%d"), i[1].strftime("%Y-%m-%d")] for i in date]
        data = [self.getData(startDate=s, endDate=e) for s, e in date]
        data.insert(0, self.getData(startDate=monday.strftime("%Y-%m-%d"), endDate=last_date.strftime("%Y-%m-%d")))
        # [print(item) for item in data]
        data_acc = [self.get_accumulation(item) for item in data]
        value = [item[1] for item in data_acc]
        # print(value)
        content = {
            # 二手房近四周成交套数
            "numberTransactSecondhandHousePastFourWeek": [
                period,
                value,
            ]
        }
        print(content)
        return content

    # 得到上个月一手房区域成交量
    def getYsfAreaData_month(self):
        print("getYsfAreaData_month...")
        resp = requests.post("http://zjj.sz.gov.cn:8004/api/marketInfoShow/getYsfCjxxGsMonthData")
        # resp = requests.post("")
        data = resp.json()["data"]
        # print(data['dataTs'])
        dataDict = {item['name']: item['value'] for item in data['dataTs']}
        # print(dataDict)
        dataDict['大鹏新区'] = dataDict.pop('大鹏')
        areaName = ['宝安', '福田', '龙岗', '罗湖', '南山', '盐田', '龙华', '光明', '坪山', '大鹏新区']
        dataDict = [{name: dataDict[name]} for name in areaName]
        # print(dataDict)
        last_date = datetime.datetime.now().date().replace(day=1) - datetime.timedelta(days=1)
        year, month = last_date.year, last_date.month
        content = {
            "year": year,
            "month": month,
            "content": dataDict,
        }
        print(content)
        self.updateData("http://114.132.235.86:3001/api/v1/firstRatioInformation", content)
        # print("YsfAreaData_month data has been successfully updated!")

    # 得到上个月二手房区域成交量
    def getEsfAreaData_month(self):
        print("getEsfAreaData_month...")
        dataDict = []
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        path = r"/opt/google/chrome/chromedriver"
        browser = webdriver.Chrome(options=options, executable_path=path)
        # 设置显式等待时间，最长等待时间为 10 秒
        wait = WebDriverWait(browser, 10)
        browser.get("http://zjj.sz.gov.cn/ris/szfdc/showcjgs/esfcjgs.aspx")
        areas = ['hypBa', 'hypFt', 'hypLg', 'hypLh', 'hypNs', 'hypYt', 'hypLhQ', 'hypGm', 'hypPs', 'hypDp']
        areaName = ['宝安', '福田', '龙岗', '罗湖', '南山', '盐田', '龙华', '光明', '坪山', '大鹏新区']
        for item, name in zip(areas, areaName):
            link_element = wait.until(EC.element_to_be_clickable((By.ID, item)))
            link_element.click()
            # 等待页面加载完成
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.ID, 'clientList2_ctl02_lblHTTS2')))
            # 提取节点的文本内容
            target_element = browser.find_element(By.ID, 'clientList2_ctl02_lblHTTS2')
            dataDict.append({name: int(target_element.text)})
            # print(f"Get data of {item} : {target_element.text}")
        # print("Result: ", dataList)
        # print("The number of areas : ", len(dataList))
        # print("The sum of data : ", sum(dataList))
        current_date = datetime.datetime.now().date()
        lastMonthDate = current_date.replace(day=1) - datetime.timedelta(days=1)
        data = {
            "year": lastMonthDate.year,
            "month": lastMonthDate.month,
            "content": dataDict,
        }
        print(data)
        self.updateData("http://114.132.235.86:3001/api/v1/ratioInformation", data)
        # browser.close()
        # print("EsfAreaData_month data has been successfully updated!")

    # 得到有记录以来所有月份的月成交量
    def getTotalData_months(self):
        print("getToalData_months...")
        # 设置日期
        start_date = datetime.date(2020, 1, 1)
        end_date = datetime.datetime.today().date()
        # end_date = datetime.date(2023, 11, 30)
        current_date = start_date
        ysf_months_data = ['ysfdata']
        esf_months_data = ['esfdata']
        months_date = ['date']
        while current_date <= end_date:
            year = current_date.year
            month = current_date.month
            _, last_day = calendar.monthrange(year, month)
            first_day_str = current_date.strftime("%Y-%m-%d")
            last_day_str = current_date.replace(day=last_day).strftime("%Y-%m-%d")
            # print(f"firstday：{first_day_str}，lastday：{last_day_str}" )
            value = self.getData(startDate=first_day_str, endDate=last_day_str)
            value = self.get_accumulation(value)
            # print(value)
            data = {
                "year": year,
                "month": month,
                "content": value[1]
            }
            self.updateData("http://114.132.235.86:3001/api/v1/soldInformation", data)
            data = {
                "year": year,
                "month": month,
                "content": value[0]
            }
            self.updateData("http://114.132.235.86:3001/api/v1/firstSoldInformation", data)
            esf_months_data.append(value[1])
            ysf_months_data.append(value[0])
            months_date.append(f"{current_date.year}-{current_date.month}")
            current_date = current_date.replace(day=1) + datetime.timedelta(days=32)
            current_date = current_date.replace(day=1)
        print(ysf_months_data)
        print(esf_months_data)
        print(months_date)
        # print(len(ysf_months_data), len(esf_months_data), len(months_date))
        # print("TotalData_months data has been successfully updated!")

    # 得到从2023年第一周开始的周成交量
    def getTotalWeeks(self):
        print("getTotalWeeks...")
        start_date = datetime.date(2023, 1, 2)
        end_date = datetime.datetime.today().date() - datetime.timedelta(days=1)
        date = []
        period = []
        data = []
        while start_date + datetime.timedelta(days=6) <= end_date:
            monday = start_date
            sunday = start_date + datetime.timedelta(days=6)
            date.append([monday, sunday])
            period.append(monday.strftime("%Y.%m.%d")[2:] + "-" + sunday.strftime("%Y.%m.%d")[2:])
            data.append(
                self.get_accumulation(self.getData(startDate=monday.strftime("%Y-%m-%d"), endDate=sunday.strftime("%Y-%m-%d"))))
            start_date = start_date + datetime.timedelta(days=7)
            # print(start_date)
        if start_date < end_date:
            date.append([start_date, end_date])
            period.append(start_date.strftime("%Y.%m.%d")[2:] + "-" + end_date.strftime("%Y.%m.%d")[2:])
            data.append(self.get_accumulation(
                self.getData(startDate=start_date.strftime("%Y-%m-%d"), endDate=end_date.strftime("%Y-%m-%d"))))
        ysf_ratio = [f"{round((data[i][0] / data[i - 1][0] - 1) * 100)}%" for i in range(1, len(data))]
        ysf_ratio.insert(0, "/")
        esf_ratio = [f"{round((data[i][1] / data[i - 1][1] - 1) * 100)}%" for i in range(1, len(data))]
        esf_ratio.insert(0, "/")
        # print(date)
        # print(period)
        # print(data)
        # print(ysf_ratio)
        # print(esf_ratio)
        # print("Weeks data has been gotten successfully!")
        ysf_content = [{"time": period[i], "number": data[i][0], "ratio": ysf_ratio[i]} for i in
                       range(len(period) - 4, len(period))]
        esf_content = [{"time": period[i], "number": data[i][1], "ratio": esf_ratio[i]} for i in
                       range(len(period) - 4, len(period))]
        print(ysf_content)
        print(esf_content)
        [self.updateData("http://114.132.235.86:3001/api/v1/firstSoldWeekInformation", item) for item in ysf_content]
        [self.updateData("http://114.132.235.86:3001/api/v1/soldWeekInformation", item) for item in esf_content]

    # 上传数据
    def updateData(self, url, data):
        resp = requests.post(url, json=data)
        # print(resp.status_code)

    # 上传数据
    def upload_data(self):    # 更新每日成交数据
        url = "http://114.132.235.86:3000/api/v1/information"
        weekday = datetime.date.today().weekday()
        current_date = datetime.datetime.now().date()
        yesterday = current_date - datetime.timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        # print(yesterday_str)
        print("running...")
        content = {
            "title": yesterday_str,
            **(self.get_lastMonth()),
            **(self.getWeeks()),
            **(self.get_threeMonthCycle()),
            **(self.get_transactionRatio()),
        }
        print("Got data!")
        # print(content)
        data = {
            "weekday": weekday + 1,
            "content": content,
        }
        # 网站抓取数据或者此处抓取并上传
        resp = requests.post(url, json=data)
        # print(resp.status_code)
        self.getTotalData_months()
        if yesterday.day is 1:
            self.getYsfAreaData_month()
            self.getEsfAreaData_month()
        if weekday is 0:
            self.getTotalWeeks()
        print("Successfully update!")

    # 获取此时exe文件内容
    def getInformation(self):
        resp = requests.get("http://114.132.235.86:3001/api/v1/information")
        data = resp.json()['data']
        # print(data)
        # print(data['soldInformation'])
        # print(data['ratioInformation'])
        [print(key, ":", data[key]) for key in data]

    # 删除对应接口中的数据
    def deleteData(self):
        url = "http://114.132.235.86:3001/api/v1/firstSoldWeekAllInformation"
        # url = "http://114.132.235.86:3001/api/v1/soldWeekAllInformation"
        # data = {
        #     "year": 2023,
        #     "month": 10,
        # }
        # data = {
        #     'time': '24.01.15-24.01.20',
        # }
        # resp = requests.delete(url, json=data)
        resp = requests.delete(url)

    # 计时器
    def job(self):
        print("job is running, time is ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.upload_data()

    def timer(self):
        sched = BlockingScheduler()
        # 截止到2023-10-31 00:00:00 每周一到周日早上0点01分运行job_function
        sched.add_job(self.job, 'cron', day_of_week='mon-sun', hour=0, minute=15, id='task')
        sched.start()
        # 移除任务
        sched.remove_job('task')


if __name__ == "__main__":
    spiderman = mySpider()
    # spiderman.upload_data()
    spiderman.timer()
    # spiderman.getInformation()