from src.server.instance import server

from src.controllers.urbanIoTController import *
from src.controllers.testController import *
from src.controllers.recifeController import *


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"

app = server.run()
