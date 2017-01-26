import requests
import statsmodels.api as sm
from ttypes import *
import datetime as dt
import pandas as pd

class Predict:
    url = "http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine15m?symbol="

    def fit(self, future):
        f_url = self.url + future
        price = requests.get(f_url)
        self.data = price.json()
        priceList = list()
        time = list()
        for item in price.json():
            time.append(dt.datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S"))
            priceList.append(float(item[1]))
        self.ori_price = pd.Series(priceList, index=time)
        self.end = time[0]
        self.start = time[-1]

        self.model = sm.tsa.ARMA(self.ori_price, (7, 1)).fit()

    def getPridict(self, num):
        result = self.model.predict()
        rradd = self.model.predict(self.start, len(self.ori_price)+num)

        # timelist = list()
        # temp = self.end
        # for i in range(len(rradd)):
        #     temp += dt.timedelta(minutes=15)
        #     timelist.append(temp)
        # rradd.index = timelist
        # result.appe

        delta = dt.timedelta(minutes=15)
        ans = list()
        count = 0
        for i in self.data:
            count += 1
            if count < len(result):
                ans.append(Price(time=i[0], price=float(i[1]), predict=float(result[count])))
            else:
                ans.append(Price(time=i[0], price=float(i[1]), predict=float(i[1])))
        temp = self.end
        for i in range(num):
            temp += delta
            ans.append(Price(time=str(temp), price=0, predict=rradd[len(self.ori_price)+i]))
        return ans

    # def calculate(self):
