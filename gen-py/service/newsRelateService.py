from newsRepository import NewRepository
from ttypes import *
import LDA
import pandas as pd
import MySQLdb as mdb
import collections
import datetime as dt
import requests
import numpy as np
import time

class newsService:
    repo = NewRepository()
    alcal = dict()
    caltime = dict()

    def relateNews(self, future):
        if self.alcal.has_key(future):
            return self.alcal[future]
        else:
            result = self.solve(future)
            self.alcal[future] = result
            self.caltime[future] = time.time()
            return result

    def solve(self, future):
        def connect():
            info = {
                "host": "10.60.42.202",
                "user": "root",
                "passwd": "GCers+518",
                "db": "news",
                "charset": "utf8"
            }
            conn = mdb.connect(**info)
            return conn

        def getDocs(d):
            docs = list()
            def solve(df):
                #print df["content"]
                if df["content"] == None:
                    docs.append("")
                else:
                    docs.append(df["content"])
            d.apply(solve, axis=1)
            return docs

        def singleDayHandler(df):
            r = collections.defaultdict(int)
            value = df["result"]
            for i in value:
                for item in i:
                    r[item[0]] += item[1]
            return pd.Series({"lda": r})

        def printDF(df):
            print df

        conn = connect()
        sql = "select * from news"
        news = pd.read_sql_query(sql, conn)
        # mask = ((d['time'] > datetime.datetime(2015, 1, 1)) & (d['time'] < datetime.datetime(2015, 12, 30)))
        # d = d[mask]

        docs = getDocs(news)

        lda = LDA.LDA()
        lda.segment(docs)

        print "start training model"
        lda.ldatrain()

        print "training model finish"

        news["result"] = lda.corpus_lda
        gt = news[["time", "result"]].groupby(pd.Grouper(freq='1D', key='time'))

        ans = gt.apply(singleDayHandler)
        # for i in range(20):
        #     print lda.model.print_topic(i)

        # future = "IF1706"
        url = "http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesDailyKLine?symbol="
        print url+future
        price = requests.get(url+future)
        if price == None:
            return list()
        price = price.json()
        if price == None:
            return list()
        tt = list()
        p = list()
        for i in price:
            tt.append(dt.datetime.strptime(i[0], "%Y-%m-%d"))
            p.append(float(i[1]))
        price = pd.DataFrame({"time": tt, "price": p})
        ans["time"] = ans.index
        total = pd.merge(price, ans, on="time")

        def getTopic(df):
            for i in range(20):
                if df["lda"].has_key(i):
                    df[str(i)] = df["lda"][i]
                else:
                    df[str(i)] = 0
            return df
        data = total.apply(getTopic, axis=1)
        data = data.drop(["lda", "time"], axis=1)
        result = np.corrcoef(data, rowvar=0)*0.5+0.5
        r0 = result[0]
        self.dd = dict()
        for i in range(20):
            # print i, r0[i+1]
            self.dd[i] = r0[i+1]
        # print dd
        topic_sort = sorted(self.dd.items(), key=lambda d: d[1], reverse=True)
        self.topic_choose = list()
        for i in range(3):
            self.topic_choose.append(topic_sort[i][0])

        self.news_list = list()
        def choose_news(df):
            global dd
            topic = df["result"]
            for i in self.topic_choose:
                if i in [x for x, y in topic]:
                    self.news_list.append(News(url=df["url"], title=df["title"], related=float(self.dd[i]), content=df["content"]))
        news.apply(choose_news, axis=1)
        return self.news_list
