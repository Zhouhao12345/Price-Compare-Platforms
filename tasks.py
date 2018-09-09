import pika
import settings as cfg
import hashlib


class Publisher(object):

    def __init__(self):
        self.routings = {}
        for git in cfg.git_map:
           git_url = git.get("git_url",False)
           git_remote_name = git.get("git_remote_name", False)
           git_branch = git.get("git_branch", False)
           if not git_url or not git_remote_name or not git_branch:
               raise Exception("Please make sure git url, path and "
                               "remote name had been typed")

           h = hashlib.md5()
           h.update((git_url+git_remote_name+git_branch).encode(
               encoding="utf-8")
           )
           route_key = h.hexdigest()
           self.routings[route_key] = git

    def start_publisher(self):
        full_url = pika.URLParameters(
            url="amqp://{username}:{passwd}@{host}:{port}{virtualhost}".format(
                username=cfg.MQ_USERNAME,
                passwd=cfg.MQ_PASSWORD,
                host=cfg.MQ_HOST,
                port=cfg.MQ_PORT,
                virtualhost=cfg.MQ_VIRTUAL_HOST
            )
        )
        self.connection = pika.BlockingConnection(full_url)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='message',
            exchange_type='direct',
            durable=True
        )
        for route_key in self.routings.keys():
            self.channel.basic_publish(exchange='message',
                                  routing_key=route_key,
                                  body="Hello", )
        self.connection.close()
