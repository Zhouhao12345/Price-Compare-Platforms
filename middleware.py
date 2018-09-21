class baseMiddleware(object):

    def process_request(self, *args, **kwargs):
        pass
    def process_response(self, *args, **kwargs):
        pass

class crosMiddleware(baseMiddleware):

    def process_response(self, response):
        response.headers["Access-Control-Allow-Origin"] = "http://www.gc.com"
        response.headers["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
        response.headers["Access-Control-Max-Age"] = "1000"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
