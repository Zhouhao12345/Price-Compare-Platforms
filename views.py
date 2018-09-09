from werkzeug.wrappers import Response

import json

from tasks import Publisher
from adapter import DeserializeHook

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
        return Response(
            json.dumps({
                "code":1,
                "message":"success"
            }),
            content_type="application/json",
            status=200
        )

    def post(self, request, **kwargs):
        agent = request.environ["HTTP_USER_AGENT"]
        payload = request.form["payload"]
        git_url, git_remote_name, git_branch = \
            DeserializeHook.deserialize(agent=agent, payload=payload)
        p = Publisher()
        p.start_publisher(
            "pull",
            git_url=git_url,
            git_remote_name=git_remote_name,
            git_branch=git_branch
        )
        return Response(
            json.dumps({
                "code": 1,
                "message": "success"
            }),
            content_type="application/json",
            status=200
        )
