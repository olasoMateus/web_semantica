from flask import Flask
from flask_restx import Api


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
                      version = '1.1',
                      title = 'Urban IoT REST Api',
                      description = 'Api para consultas da ontologia Urban IoT',
                      doc = '/docs'
        )

    def run(self):
        self.app.run(
            debug = False
        )

server = Server()