FILTERS = []
ENDP_COUNT = 0

class Filter(object):
    def __init__(self):
        self.urls = []
        self.filter_all = False
        self.order = 0

    def filter(self, request, response): pass

    def _continue(self, request, response):
        return {"request": request, "response": response}