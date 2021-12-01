import socketio
from urllib.parse import parse_qs
from beanie import PydanticObjectId


from ..routers.game import Game
from .queries import get_or_create_game_round

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
sio_app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    print("here Now")
    game_id = parse_qs(environ['QUERY_STRING']).get("game_id")[0]
    game = await Game.get(PydanticObjectId(game_id))
    game_round = await get_or_create_game_round(game_id)

    send_data = {
        "min_bet": game.min_bet,
        "max_bet": game.max_bet,
        "name": game.name,
        "game_round_id": str(game_round.id)
    }

    sio.enter_room(sid, game_id)
    await sio.emit("on_connect_data", send_data, to=sid)
    print("sadasdsdda")


@sio.event
async def scan_card(sid, data):
    card = data.get('card')
    print(data)
    await sio.emit("sdasd", data)


@sio.event
async def disconnect(sid):
    print("I'm disconnected!")

