from app import app
from wsgiref.simple_server import make_server

# demo server
if __name__ == "__main__":
    httpd = make_server("127.0.0.1", 8000, app)
    httpd.serve_forever()