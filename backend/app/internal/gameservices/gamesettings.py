from fastapi import HTTPException, status
from datetime import datetime
from app.routers.game import Game, Round


async def check_game_bets(game):
    """
    checks if min bet is lower than max bet
    :param game: game information
    :return: raise exception if min bet is higher than max bet
    """
    if game.min_bet > game.max_bet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Min bet can not be higher than max bet",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return None


async def check_game_id(game_id: str):
    """
    Checks if the game exists at all with specific ID
    :param game_id: str - gets id of the game and raise exception if
    it does not exists
    :return: str,  the current game id
    """
    current_game_id = await Game.get(game_id)
    if not current_game_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect Game ID",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return str(current_game_id.id)


async def check_round_id(round_id: str):
    """
    Checks if the round exists at all with specific ID
    :param round_id: str, gets id of the round and raise exception if
    it does not exists
    :return: tuple, the round id and game id it belongs
    """
    current_round_id = await Round.get(round_id)
    if not current_round_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect Game ID",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return str(current_round_id.id), str(current_round_id.game_id)


async def get_current_deck(game_id: str):
    """
    Functions gets the deck of the specific game with id
    :param game_id: checks if game exists
    :return: list, of the deck cards of the current game which are not handled yet
    """
    current_deck = await Game.get(game_id)
    if not current_deck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect Game ID",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return list(current_deck.deck.values())[0]


async def deck_update(game_id: str, deck: list):
    """
    Updates the deck in the game, which are not handeled yet after dragon and tiget play
    :param game_id: str, game where cards should be updated
    :param deck: card after dragon and tiger play
    :return: updates game deck
    """
    deck_amend = await Game.get(f'{game_id}')
    deck_amend.deck = {'cards': deck}
    return await deck_amend.save()


async def check_round_time(round_id):
    """
    checks the round time is finished or not, if yes raise exception
    :param round_id: check the current round
    :return: none, if the player can bet
    """
    round_time = await Round.get(round_id)
    if round_time.finish_time < datetime.timestamp(datetime.now()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Round time is out, You can not bet now",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return None


async def check_deposit(total_bet, current_deposit):
    """
    checks if current user have enough money to bet
    :param total_bet: int, from total bet
    :param current_deposit: current money on current users balance
    :return: None, if exception is not raised
    """
    if current_deposit < float(total_bet):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not enough Money",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return None


async def update_balance_minus(total_bet, current_users):
    """
    Updates the balance of the users after the betting
    :param total_bet: int of the total bet on current round
    :param current_users: current users Document
    :return: updates current users balance
    """
    current_users.deposit -= total_bet
    return await current_users.save()



async def update_balance_plus(deposit_in, current_users):
    """
    Updates / adding the balance of the users
    :param deposit_in: float / int money to be added on the balance
    :param current_users: current users Document
    :return: saves the updated balance
    """
    current_users.deposit += deposit_in
    return await current_users.save()


async def check_min_max_bet(gameplayer):
    """
    Checks if the currnet bets are lower or higher of the game
    :param gameplayer: Document of gameplayer
    :return: if not in max and min bet raises erro else returns none
    """
    game_bet = await Game.get(gameplayer.game_id)

    if gameplayer.dragon_bet != 0 and gameplayer.dragon_bet < game_bet.min_bet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dragon bet is lower than min bet",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if gameplayer.dragon_bet > game_bet.max_bet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dragon bet is higher than max bet",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if gameplayer.tiger_bet != 0 and gameplayer.tiger_bet < game_bet.min_bet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tiger bet is lower than min bet",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if gameplayer.tiger_bet > game_bet.max_bet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tiger bet is higher than max bet",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if gameplayer.tie_bet != 0 and gameplayer.tie_bet < game_bet.min_bet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tie bet is lower than min bet",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if gameplayer.tie_bet > game_bet.max_bet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tie bet is higher than max bet",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return None


