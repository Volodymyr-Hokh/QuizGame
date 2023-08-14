from sanic import Sanic
from sanic.response import text, file, json, html

from sanic import Request, Websocket

from gateway2 import EventHandler


app = Sanic("MyHelloWorldApp")
app.static("/", "./build")

handler = EventHandler()
app.add_websocket_route(handler.handle, '/ws')

@app.get("/route")
async def route(request):
    return json({"websocket": f'wss://{request.headers.host}/ws'})

@app.get("/")
async def index(request):
    with open("./build/index.html") as f:
        return html(f.read())

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)