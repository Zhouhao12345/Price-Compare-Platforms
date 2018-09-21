from werkzeug.wrappers import Request
from werkzeug.exceptions import HTTPException
from urls import urls_patterns
from middleware_warp import middlewareWrapper

class App(object):

    def __init__(self):
        self.url_map = urls_patterns

    @middlewareWrapper
    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return endpoint()(request, **values)
        except HTTPException as e:
            return e

    @Request.application
    def __call__(self, request):
        return self.dispatch_request(request)

app = App()
