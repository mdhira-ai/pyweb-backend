from fastapi import FastAPI, WebSocket, WebSocketException
from socket_pro import socketio
import uvicorn
import asyncio
from mytasks import MTask


socket = socketio()
app = FastAPI()

task1 = MTask(socket=socket, messageport="nmap")
task2 = MTask(socket=socket, messageport="ping")


@app.websocket("/ws/122")
async def socketserver(websocket: WebSocket):
    await socket.connect(websocket=websocket)

    try:

        while True:
            data = await websocket.receive_json()
            print(data["data_type"])

            match data["data_type"]:
                case "nmap-start":
                    cmd = "sudo nmap -v -A scanme.nmap.org"
                    await task1.taskrun(cmd=cmd)

                case "nmap-stop":
                    await task1.stop()


                case "ping-start":
                    cmd= "ping google.com"
                    await task2.taskrun(cmd=cmd)

                case "ping-stop":
                    await task2.stop()


    except:
        print("client disconnect")
        socket.disconnect(websocket=websocket)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
