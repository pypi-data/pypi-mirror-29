from gofri.lib.decorate.tools import _wrap_http
from gofri.lib.http.filter import FILTERS
from gofri.lib.http.handler import RequestHandler


class GofriFilter:
    def __init__(self, urls=[], filter_all=False, order=0):
        self.urls = urls
        self.filter_all = filter_all
        self.order = order

    def __call__(self, cls):
        filter_obj = cls()
        filter_obj.urls = self.urls
        filter_obj.filter_all = self.filter_all
        filter_obj.order = self.order
        FILTERS.append(filter_obj)

class GET(RequestHandler):
    def __init__(self, path, headers=None, body=None, json=None):
        super().__init__(headers, body, json)
        self.path = path

    def __call__(self, func):
        return _wrap_http(self.path, ["GET"], func)


class POST(RequestHandler):
    def __init__(self, path, headers=None, body=None, json=None):
        super().__init__(headers, body, json)
        self.path = path

    def __call__(self, func):
        return _wrap_http(self.path, ["POST"], func)


class HEAD(RequestHandler):
    def __init__(self, path, headers=None, body=None, json=None):
        super().__init__(headers, body, json)
        self.path = path

    def __call__(self, func):
        return _wrap_http(self.path, ["HEAD"], func)


class PUT(RequestHandler):
    def __init__(self, path, headers=None, body=None, json=None):
        super().__init__(headers, body, json)
        self.path = path

    def __call__(self, func):
        return _wrap_http(self.path, ["PUT"], func)


class DELETE(RequestHandler):
    def __init__(self, path, headers=None, body=None, json=None):
        super().__init__(headers, body, json)
        self.path = path

    def __call__(self, func):
        return _wrap_http(self.path, ["DELETE"], func)
