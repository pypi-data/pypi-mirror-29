class RequestHandler(object):
    def __init__(self, headers=None, body=None, json=None):
        self.path = None
        self.headers = headers
        self.body = body
        self.json = json
