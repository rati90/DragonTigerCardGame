import socketio
from urllib.parse import parse_qs
from beanie import PydanticObjectId


from ..routers.game import Game, Round
from .queries import get_or_create_game_round
from ..internal.gameservices.gamelogic import find_a_winner, cards

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
sio_app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    game_id = parse_qs(environ['QUERY_STRING']).get("game_id")[0]
    game = await Game.get(PydanticObjectId(game_id))
    game_round = await get_or_create_game_round(game_id)
    send_data = {
        "min_bet": game.min_bet,
        "max_bet": game.max_bet,
        "name": game.name,
        "game_round_id": str(game_round.id),
        "start_timestamp": 15
    }
    sio.enter_room(sid, game_id)
    await sio.emit("on_connect_data", send_data, to=sid)
    print("Connected")


@sio.event
async def scan_card(sid, data):
    game_round = await Round.get(PydanticObjectId(data['game_round_id']))
    card = data['card']
    if game_round.dragon_card == None:
        game_round.dragon_card = card
        game_round.card_passed += 1
        await game_round.save()
        await sio.emit("send_dragon_card", {"card": card}, room=game_round.game_id)

    else:
        game_round.tiger_card = card
        game_round.card_passed += 1
        await game_round.save()
        await sio.emit("send_tiger_card", {"card": card}, room=game_round.game_id)

        game_round.winner = await find_a_winner(game_round.dragon_card, game_round.tiger_card, cards)
        await game_round.save()
        await sio.emit('send_winner', {'winner': game_round.winner}, room=game_round.game_id)
        print(game_round.winner)

        print(game_round.id)
        print(game_round.game_id)
        print(data)


@sio.event
async def place_bet(sid, data):
    amount = data['amount']
    type = data['type']
    print(amount, type)



@sio.event
async def receive_target(sid, data):
    target = data.get('target')
    await sio.emit("sdasd", data)


@sio.event
async def disconnect(sid):
    print("Disconnected!")


