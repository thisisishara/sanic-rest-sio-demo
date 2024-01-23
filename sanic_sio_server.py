from sanic import Sanic, request, response
from sanic.log import logger
from sanic.response import json, text
from sanic_cors import CORS
import socketio
# from socketio.exceptions import ConnectionRefusedError


app = Sanic(__name__)
CORS(app)
sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='sanic')
sio.attach(app, socketio_path="/socket.io")

clinet_count = 0
client_info = dict()


@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")

@sio.event
async def set_client_info(sid, data):
    global clinet_count
    global client_info

    logger.info(f"data: {data}")
    secret = data.get("secret")
    room_id = data.get("roomId")

    # connect to the room temporarily till authenticated
    await sio.enter_room(sid, room_id)
    logger.info(f"sid {sid} joined the room: {room_id}")

    # dummy auth
    if secret == "secret":
        client_info[sid] = {"data": data}
        clinet_count += 1

        await sio.emit("auth_success", f"Client {sid} authenticated!", room=room_id)
        logger.info(f"Client {sid} authenticated!")
    else:
        await sio.emit("auth_failure", f"Authentication failed for client {sid}", room=room_id)
        logger.info(f"Authentication failed for client {sid}")
        await sio.disconnect(sid)
    
    logger.info(f"Active clients: {clinet_count}")
    
# # disabled due to auth
# @sio.event
# async def join(sid, room_id):
#     logger.info(f"sid {sid} joined the room: {room_id}")
#     await sio.enter_room(sid, room_id)


@sio.event
async def disconnect(sid):
    global clinet_count
    global client_info
    
    if sid in client_info:
        del client_info[sid]
        clinet_count -= 1
    
    logger.info(f"Client disconnected: {sid}")
    logger.info(f"Active clients: {clinet_count}")


@app.post("/message")
async def receive_message(request):
    message = request.json.get("message", "")
    room_id = request.json.get("room_id", "")
    logger.info(f"/message route, room_id: {room_id}")
    await sio.emit("message", f"FROM SERVER: {message}", room=room_id)
    return json({"status": "Message received and broadcasted"})

@app.route("/")
async def index(request):
    logger.info(f"/root route")
    return text("hi")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
