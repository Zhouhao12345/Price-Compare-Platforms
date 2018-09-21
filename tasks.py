import pika
import settings as cfg
import hashlib


class Publisher(object):

    @staticmethod
    def md5_route_key(git_url="",git_remote_name="", git_branch=""):
        if not git_url or not git_remote_name or not git_branch:
            raise Exception("Please make sure git url, path and "
                            "remote name had been typed")

        h = hashlib.md5()
        h.update((git_url + git_remote_name + git_branch).encode(
            encoding="utf-8")
        )
        return h.hexdigest()

    def start_publisher(self, order, **kwargs):
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
        route_key = Publisher.md5_route_key(**kwargs)
        self.channel.basic_publish(exchange='message',
                                  routing_key=route_key,
                                  body=order, )
        self.connection.close()
