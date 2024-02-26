from fastapi import FastAPI, WebSocket
from websocket import echo
from routers.api import router as api_router
from routers.websocket import router as websocker_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)
app.include_router(websocker_router)

@app.get("/")
async def get():
    return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>WebSocket Test</title>
            <script>
                var socket = new WebSocket("ws://localhost:5000/ws");
                socket.onmessage = function(event) {
                    var messages = document.getElementById("messages");
                    messages.innerHTML += "<p>" + event.data + "</p>";
                };
                function sendMessage() {
                    var messageInput = document.getElementById("message_input");
                    var message = messageInput.value;
                    socket.send(message);
                    messageInput.value = "";
                }
            </script>
        </head>
        <body>
            <div id="messages"></div>
            <input type="text" id="message_input" placeholder="Type a message...">
            <button onclick="sendMessage()">Send</button>
        </body>
        </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await echo(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
