from werkzeug.wrappers import Response

import json

from tasks import Publisher

class View(object):
    def __init__(self):
        self.method_view = {
            "GET": getattr(self, "get"),
            "POST": getattr(self, "post")
        }

    def __call__(self, request, **kwargs):
        return self.method_view.get(request.method, "other")(request, **kwargs)

    def other(self, *args, **kwargs):
        return Response("Request Method Not Support")

class Test(View):

    def get(self, request, **kwargs):
        p = Publisher()
        p.start_publisher(order="pull")
        return Response(
            json.dumps({
                "code":1,
                "message":"success"
            }),
            content_type="application/json",
            status=200
        )

    def post(self, request, **kwargs):
        for key , value in request.form.items():
             print(key+":"+value)
        return Response(
            json.dumps({
                "code": 1,
                "message": "success"
            }),
            content_type="application/json",
            status=200
        )
