#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from six import itervalues
import MySQLdb
from datetime import *

class NewRepository():
    def __init__(self):
        '''
        kwargs = {
            'host':'locolhost',
            'user':'root',
            'passwd':'163613',
            'db':'news',
            'charset':'utf8'
        }
        :param kwargs:
        :return:
        '''
        kwargs = {
            'host': '10.60.42.202',
            'user': 'root',
            'passwd': 'GCers+518',
            'db': 'news',
            'charset': 'utf8'
        }

        host = kwargs['host']
        username = kwargs['user']
        passwd = kwargs['passwd']
        db = kwargs['db']
        charset = kwargs['charset']

        self.connection = False
        try:
            self.conn = MySQLdb.connect(host = host, user = username, passwd = passwd, db = db, charset = charset)
            self.cursor = self.conn.cursor()
            self.cursor.execute("set names " + charset)
            self.connection = True
        except Exception, e:
            print "Cannot connect to mysql!/n", e
    #
    # def escape(self, string):
    #     return '%s'% string
    #
    # def add(self, tablename=None, **values):
    #     if self.connection:
    #         tablename = self.escape(tablename)
    #
    #         if values:
    #             if not self.checkUrl(values["url"]):
    #                 return False
    #             _keys = ",".join(self.escape(i) for i in values)
    #             _value = ",".join(['%s']*len(values))
    #             sql_query = "insert into %s (%s) values (%s)" % (tablename, _keys, _value)
    #             print "add new item"
    #         else:
    #             sql_query = "replace into %s default values" % tablename
    #
    #         try:
    #             if values:
    #                 self.cursor.execute(sql_query, list(itervalues(values)))
    #             else:
    #                 self.cursor.execute(sql_query)
    #             self.conn.commit()
    #             return True
    #         except Exception, e:
    #             print "Error ", e
    #             return False

    # def excute(self, sql_query, data):
    #     try:
    #         self.cursor.execute(sql_query, data)
    #         self.conn.commit()
    #     except Exception, e:
    #         print "Error", e
    #         return False

    # def checkUrl(self, url):
    #     sqlcode = "select url from news where url='%s'" % url
    #     self.cursor.execute(sqlcode)
    #     news = self.cursor.fetchall()
    #     if len(news) > 0:
    #         return False
    #     else:
    #         return True


if __name__ == '__main__':
    sql = SQL()
    item = {
        'url': 'sovesf',
        'title': 'hello',
        'time': str(datetime.now()),
    }

    #sql.add("newsinfo", **item)

    result = {
        'url': 'sovesf',
        'text': 'sadfsgeegge'
    }
#     sql_query = "update newsinfo set text=%s where url=%s"
#     data = (result["text"], result["url"])
#     print sql_query
#     sql.excute(sql_query, (result["text"], result["url"]))
    sql.selectByUrl("http://www.chinadaily.com.cn/business/2014-1/content_18925442.htm")