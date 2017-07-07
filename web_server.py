import tornado.ioloop
import tornado.web
import tushare as ts
import numpy as np


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        try:
            code = self.get_argument('code')
            ktype = self.get_argument('ktype', 'D')
            count = self.get_argument('count', '100')
            df = ts.get_k_data(code, ktype=ktype).tail(int(count))
            print(df)
            # df = df[['date', 'open', 'close']]
            self.write(df.to_json(orient='records', force_ascii=False))

        except tornado.web.MissingArgumentError:
            self.write('必须提供code参数')

            # df = ts.get_hist_data(code)
            # self.write(df.to_json(orient='records', force_ascii=False))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


def KDJ(date, n=9, m1=3, m2=3):
    datelen = len(date)
    array = np.array(date)
    kdjarr = []
    for i in range(datelen):
        if i - n < 0:
            b = 0
        else:
            b = i - n + 1
        rsvarr = array[b:i + 1, 0:5]
        rsv = (float(rsvarr[-1, -1]) - float(min(rsvarr[:, 3]))) / (
            float(max(rsvarr[:, 2])) - float(min(rsvarr[:, 3]))) * 100
        if i == 0:
            k = rsv
            d = rsv
        else:
            k = 1 / float(m1) * rsv + (float(m1) - 1) / m1 * float(kdjarr[-1][2])
            d = 1 / float(m2) * k + (float(m2) - 1) / m2 * float(kdjarr[-1][3])
        j = 3 * k - 2 * d
        kdjarr.append(list((rsvarr[-1, 0], rsv, k, d, j)))
    return kdjarr


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
