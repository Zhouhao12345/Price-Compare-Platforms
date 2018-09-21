from elasticsearch import Elasticsearch
from settings import ES_PORT, ES_HOST

class EsEngine(Elasticsearch):

    def search(self, **kwargs):
        result_es = super(EsEngine, self).search(
            **kwargs
        )
        result_list = [r["_source"] for r in result_es["hits"]["hits"]]
        max_size = result_es["hits"]["total"]
        return result_list, max_size

    def __call__(self, *args, **kwargs):
        es_host =  kwargs.get("host", ES_HOST)
        es_port = kwargs.get("port", ES_PORT)
        return EsEngine(
            hosts=[{
                "host": es_host,
                "port": es_port,
            }]
        )


es = EsEngine()
