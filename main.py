from fastapi import FastAPI, WebSocket, WebSocketException
from socket_pro import socketio
import uvicorn
import asyncio
from mytasks import MTask


socket = socketio()
app = FastAPI()

task1 = MTask()


@app.websocket("/ws/122")
async def socketserver(websocket: WebSocket):
    await socket.connect(websocket=websocket)


    try:

        while True:
            data = await websocket.receive_json()
            print(data['data_type'])

            match data['data_type']:
                case "start":
                    await task1.taskrun(socket)


                case "stop":
                    await task1.stop()
                    # Default case for any other data type

    except:
        print('client disconnect')
        socket.disconnect(websocket=websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
