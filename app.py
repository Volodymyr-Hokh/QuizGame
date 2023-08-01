from sanic import Sanic
from sanic.response import text, file

from sanic import Request, Websocket

from gateway2 import EventHandler

handler = EventHandler()

app = Sanic("MyHelloWorldApp")
app.static("/", "./build")

app.add_websocket_route(lambda r, w: handler.handle(w, None), "/ws")

# @app.get("/")
# async def index(request):
#     return await file("frontend/index.html")


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)