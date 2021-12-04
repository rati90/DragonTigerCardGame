import socketio
from urllib.parse import parse_qs
from beanie import PydanticObjectId

from ..routers.game import Game, Round, GamePlayer
from .queries import get_or_create_game_round, get_or_create_game_player, add_bets_in, give_all_winner_money
from ..internal.gameservices.gamelogic import find_a_winner_card, cards

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
        await sio.emit("send_tiger_card", {"card": card}, room=game_round.game_id)

        game_round.winner = await find_a_winner_card(game_round.dragon_card, game_round.tiger_card, cards)

        await give_all_winner_money(game_round)

        await sio.emit('send_winner', {'winner': game_round.winner}, room=game_round.game_id)
        print(game_round)


@sio.event
async def place_bet(sid, data):
    bet_amount = int(data['amount'])
    bet_card = data['type']
    round_id = data['round_id']['game_round_id']

    round = await Round.get(PydanticObjectId(round_id))

    gamer_in = await get_or_create_game_player(round)

    await add_bets_in(gamer_in, bet_card, bet_amount)

    print(gamer_in)


@sio.event
async def disconnect(sid):
    print("Disconnected!")
