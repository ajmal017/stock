import tornado.ioloop
import tornado.web
import tushare as ts


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


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
