from werkzeug.wrappers import Response
from models.backend import es

import json
import math

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
        name_key_words = request.form["name_key_words"]
        size = request.form["size"]
        page = request.form["page"]

        result_list, max_size = es().search(
            index="products_list_spider",
            size=size,
            from_=(int(page)-1)*int(size),
            body={
                "query": {
                    "match": {
                        "name": name_key_words
                    }
                }
            }
        )
        return Response(
            json.dumps({
                "code": 1,
                "message": "success",
                "data": {
                    "product_list": result_list,
                    "max_page": math.ceil(int(max_size) / int(size)),
                    "cur_page": int(page)
                }
            }),
            content_type="application/json",
            status=200
        )
