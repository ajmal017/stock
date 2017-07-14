# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tushare as ts


# import numpy as np
# from wxpy import *
# from wechat_sender import *

class GetCurrentPrice(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, stock_id):
        # df = ts.get_today_all()
        # print(df)
        # df = df.ix[df.code == stock_id]
        df = ts.get_realtime_quotes(stock_id)
        print(df)
        self.write(df.to_json(orient='records', force_ascii=False))


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    """
    获取k线数据
      注意：
      如果指定了start或者end，即使end日期远大于当前日起，返回的数据不含当天的k线数据，这个需要修正一下
      
    return
    -------
      DataFrame
          date 交易日期 (index)
          open 开盘价
          high  最高价
          close 收盘价
          low 最低价
          volume 成交量
          amount 成交额
          turnoverratio 换手率
          code 股票代码
    """

    def get(self):
        try:
            code = self.get_argument('code')
            ktype = self.get_argument('ktype', 'D')
            count = self.get_argument('count', '100')
            start = self.get_argument('start', '')
            end = self.get_argument('end', '')
            if start == '' or end == '':
                df = ts.get_k_data(code, ktype=ktype, autype='qfq').tail(int(count))
            else:
                df = ts.get_k_data(code, ktype=ktype, autype='qfq', start=start, end=end)
                # df1 = ts.get_k_data(code, ktype=ktype, autype='qfq').tail(int(count))
            print(df)
            # df = df[['date', 'open', 'close']]
            self.write(df.to_json(orient='records', force_ascii=False))

        except tornado.web.MissingArgumentError:
            self.write('必须提供code参数')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/getCurrentPrice/(.*)', GetCurrentPrice),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
