# sanic-rest-sio-demo
A demo sanic server with a REST API and socketio server

## How it works
- `Sanic` server exposes a `simple REST API` and also runs a `socketio` websockets server
- The JS client provided first gets connected to the socketio server.
- The socketio server then authenticates the client and connects them to a `room` if a valid `secret` is provided.
- After the socketio connection is established, whenever the client sends a message to the REST endpoint `/message` gets emitted to the room the client is connected.
- The emitted message is then read by the client and shown in realtime in the frontend.

## How to run
- Create a venv and activate it.
- Run `pip install -r requirements.txt` from the project root.
- Run `python sanic_sio_server.py` on windows, `python3 sanic_sio_server.py` on linux.
- Open up the `sanic_sio_client.html` in a browser, preferrably chrome.
- Send a `message` and observe.

[!NOTE] To mimic a auth failure scenario, change the `const secret = "secret";` to `const secret = "secrett";` and refresh the client.
