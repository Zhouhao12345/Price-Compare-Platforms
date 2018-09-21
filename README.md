# autogit
Distributed  Webhook Server
Allow you build one webhook Server to service all coding_pull tasks.
Note: Before start, You should have your own message queue (ony support rabbitmq) on any broker server.

Webhook Request Gateway Build
1. pip install -r requirements.txt
2. vim settings
3. gunicorn app:app

webhook broker worker build
1. pip install -r requirements.txt
2. vim task/config.py
3. cd task & python worker.py
