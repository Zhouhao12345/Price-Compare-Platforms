from multiprocessing import Manager, Pool
import hashlib
import time
import os
import git
import random

from mq_server import ExampleConsumer
from config import *

def start_consumer(queue_map):
    example = ExampleConsumer(
        "amqp://{username}:{passwd}@{host}:{port}{virtualhost}".format(
            username=MQ_USERNAME,
            passwd=MQ_PASSWORD,
            host=MQ_HOST,
            port=MQ_PORT,
            virtualhost=MQ_VIRTUAL_HOST
        ), queue_map, QUEUE_NAME)
    try:
        example.run()
    except KeyboardInterrupt:
        example.stop()

def pull(cd, q, index):
    while True:
        with cd:
            if q.empty():
                cd.wait()
            else:
                q.get_nowait()
                try:
                    git_detail_info = git_map[index]
                    git_path = git_detail_info.get("git_path")
                    git_remote_name = git_detail_info.get("git_remote_name")
                    git_branch = git_detail_info.get("git_branch")
                    git_url = git_detail_info.get("git_url")
                    print(git_branch)
                    empty_repo = git.Repo.init(git_path)
                    remote_list = empty_repo.remotes
                    origin = remote_list.origin if len(remote_list) > 0 else False
                    if not origin or not origin.exists():
                        origin = empty_repo.create_remote(
                            git_remote_name,
                            git_url
                        )
                        origin.fetch()
                    empty_repo.create_head(git_branch,
                                           getattr(origin.refs, git_branch))
                    getattr(empty_repo.heads, git_branch).set_tracking_branch(
                        getattr(origin.refs, git_branch))
                    getattr(empty_repo.heads, git_branch).checkout()
                    origin.pull()

                except Exception as e:
                    print(e)

if __name__ == "__main__":
    manager = Manager()
    queue_map = {}
    cd = manager.Condition()
    with Pool(len(git_map) + 1) as p:
        for index, git in enumerate(git_map):
            queue = manager.Queue()
            cd = manager.Condition()
            git_url = git.get("git_url", False)
            git_remote_name = git.get("git_remote_name", False)
            git_branch = git.get("git_branch", False)
            if not git_url or not git_remote_name or not git_branch:
                raise Exception("Please make sure git url, path and "
                                "remote name had been typed")

            h = hashlib.md5()
            h.update((git_url + git_remote_name + git_branch).encode(
                encoding="utf-8")
            )
            route_key = h.hexdigest()
            queue_map[route_key] = (queue, cd)
            p.apply_async(pull, (cd,queue, index))

        p.apply_async(start_consumer, (queue_map,))

        p.close()
        p.join()
