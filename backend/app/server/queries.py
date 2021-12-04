from ..routers.game import Round, GamePlayer
from datetime import datetime


async def get_or_create_game_round(game_id: str):
    """
    Checks if the round exists and time is not finished yet.
    :param game_id: str of the game id
    :return: returns the round that exists or creates new one
    """
    game_round = await Round.find_one(Round.game_id == game_id,
                                      Round.finish_time > datetime.timestamp((datetime.now()))
                                      )
    if game_round:
        return game_round

    game_round = Round(game_id=game_id, finish_time=datetime.timestamp((datetime.now())) + 15)
    return await game_round.save()


async def get_or_create_game_player(round):
    """
    When betting checks if the game playes exists
    if not created one
    :param round: document of the current round
    :return: returns existed game or creates the one and saves
    """
    gamer_in = await GamePlayer.find_one(GamePlayer.game_id == round.game_id,
                                         GamePlayer.round_id == str(round.id))
    if gamer_in:
        return gamer_in

    gamer_in = GamePlayer(game_id=round.game_id, round_id=str(round.id))
    return await gamer_in.save()


async def add_bets_in(gamer_in, bet_card, bet_amount):
    """
    Add bets the amount is choice from the front
    :param gamer_in: Currtenr GamePlayer
    :param bet_card: str the card it is betting
    :param bet_amount: int the amount it is betting
    :return: saves in GamePlayer Document
    """
    gamer_in.total_bet += bet_amount

    if bet_card == "dragon":
        gamer_in.dragon_bet += bet_amount
    elif bet_card == "tiger":
        gamer_in.tiger_bet += bet_amount
    elif bet_card == "tie":
        gamer_in.tie_bet += bet_amount

    return await gamer_in.save()


async def give_all_winner_money(game_round):
    """
    find all the player who betted at all.
    then find who betted on winner cards and gives money the persons wins
    :param game_round: Document of current round
    :return: return saves round that is finished after giving money.
    """

    async for result in GamePlayer.find(GamePlayer.round_id == str(game_round.id),
                                                GamePlayer.total_bet > 0):
        if game_round.winner == 'dragon' and result.dragon_bet > 0:
            result.money_won = result.dragon_bet * 2
        if game_round.winner == 'tiger' and result.tiger_bet > 0:
            result.money_won = result.tiger_bet * 2
        if game_round.winner == 'tie' and result.tiger_bet > 0:
            result.money_won = result.tiger_bet * 8

        print(result)
        await result.save()

    return await game_round.save()
