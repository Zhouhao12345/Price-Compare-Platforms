FROM python:3.6.5

RUN mkdir -p /usr/app

WORKDIR /usr/app
COPY . .
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

CMD gunicorn -w2 app:app -b 0.0.0.0:8000


