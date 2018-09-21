from settings import MIDDLEWARE_LIST
from import_path import import_string

class middlewareWrapper(object):
    def __init__(self, func):
        self.middleware_list = [
            import_string(mid)() for mid in MIDDLEWARE_LIST
        ]
        self.func = func

    def __call__(self, *args, **kwargs):
        for middleware in self.middleware_list:
            getattr(middleware, "process_request")(*args, **kwargs)
        response =  self.func(*args, **kwargs)
        for middleware in self.middleware_list:
            getattr(middleware, "process_response")(response)
        return response

    def __get__(self, instance, owner):
        from functools import partial
        return partial(self.__call__, instance)