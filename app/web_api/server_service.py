import logging
import requests
import json
import multiprocessing

from requests.exceptions import ConnectionError

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


import version
_logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_personal_json(self, data, websocket: WebSocket):
        await websocket.send_text(json.dumps(data))

    async def send_error(self, error_message: str, websocket: WebSocket, data: dict=None):
        data = data or {}
        await self.send_personal_json({
            'error': error_message,
            **data
        }, websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
manager = ConnectionManager()


class WebsocketHandler:
    api_version: str = ''
    _instance = None

    def __init__(self, websocket: WebSocket, connection_manager: ConnectionManager):
        self.websocket = websocket
        self.manager = connection_manager

    async def process(self, data):
        raise NotImplementedError


websocket_handlers = []
def websocket_handler(cls):
    websocket_handlers.append(cls)

def _get_websocket_handler(api_version, websocket):
    for handler in websocket_handlers:
        if handler.api_version == api_version:
            return handler(websocket, manager)
    raise Exception(f"Websocket handler not found for api version: {version}, maybe you need to update Viindoo Sign Client.")

@app.get("/")
async def get():
    return HTMLResponse('Viindoo Sign Client')

@app.get('/viin_local_sign_test_connection')
async def test_connection():
    return HTMLResponse('ok')

@app.get('/version')
async def get_version():
    return {
        'version': version.__version__,
    }


@app.websocket("/ws/{api_version}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, api_version: str, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            try:
                handler = _get_websocket_handler(api_version, websocket)
                await handler.process(data)
            except Exception as e:
                await manager.send_error('Internal Server Error', websocket)
                raise
    except WebSocketDisconnect:
        manager.disconnect(websocket)


def _is_service_api_started():
    try:
        res = requests.get('http://localhost:8169', verify=False)
        if res.status_code == 200:
            return True
    except (ConnectionRefusedError, ConnectionError):
        return False

PORT = 8169
API_URL = "http://localhost:8169"
is_started = _is_service_api_started()
api_service_process: multiprocessing.Process = None


def _start():
    import uvicorn
    uvicorn.run(
        app,
        host="localhost", port=PORT,
        log_level="info", access_log=True, log_config=None
    )
    _logger.info('API is Started')


def start_api_service(new_process=True):
    global api_service_process
    global is_started
    if not _is_service_api_started():
        if new_process:
            api_service_process = multiprocessing.Process(target=_start)
            api_service_process.start()
        else:
            _start()
        is_started = True


def stop_api_service():
    global is_started
    global api_service_process
    if not api_service_process:
        return
    api_service_process.kill()
    is_started = False
    _logger.info('API is stopped')
