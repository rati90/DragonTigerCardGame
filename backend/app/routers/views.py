from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm


from app.routers.game import Game, Round, GamePlayer, User
from .userout import UserOut
from ..config import settings
from ..internal.gameservices.gamesettings import check_game_id, check_round_id, \
    check_round_time, check_deposit, update_balance_minus, update_balance_plus, check_min_max_bet,  \
    check_game_bets
from ..internal.gameservices.gamelogic import bet_win

from ..internal.services.authontication import get_password_hash, authenticate_user, create_access_token, \
    get_current_user

router = APIRouter(prefix="")

time_stamp_now = datetime.timestamp(datetime.now())

# -------------- Game -------------------------

@router.post('/game', tags=["Game"])
async def new_game(game_data: Game):
    await check_game_bets(game_data)
    return await game_data.save()


@router.get('/allgames/', tags=["Game"])
async def show_all_game():
    return await Game.find_all().to_list()
    #return await Game.find_all().delete()


# ------------- Round ------------------------

@router.post('/round', tags=['Round'])
async def new_round(round: Round, game_id: str):
    round.game_id = await check_game_id(game_id)

    round.start_time = time_stamp_now
    round.finish_time = round.start_time + 100


    if round.finish_time >= time_stamp_now:
        round.finish = False
    else:
        round.finish = True
        print("time is out")

    return await round.save()


@router.get('/round/{round_id}', tags=['Round'])
async def show_round(round_id: str):
    return await Round.get(round_id)


# ------------- GamePlayer ------------------------

@router.post('/gamer_in_round', tags=['GamePlayer'])
async def new_hand(gamer_in_round: GamePlayer, round_id: str, current_user: User = Depends(get_current_user)):
    gamer_in_round.round_id, gamer_in_round.game_id = await check_round_id(round_id)

    await check_round_time(round_id)

    gamer_in_round.total_bet = gamer_in_round.dragon_bet + gamer_in_round.tiger_bet + gamer_in_round.tie_bet

    await check_min_max_bet(gamer_in_round)

    await check_deposit(gamer_in_round.total_bet, current_user.deposit)

    await update_balance_minus(gamer_in_round.total_bet, current_user)

    winner_card = await Round.get(round_id)
    win = await bet_win(gamer_in_round.dragon_bet,
                        gamer_in_round.tiger_bet,
                        gamer_in_round.tie_bet,
                        winner_card.winner)

    gamer_in_round.money_won = sum(win)

    await update_balance_plus(sum(win), current_user)

    current_user.game_history += [[{'date': time_stamp_now}, dict(gamer_in_round)]]
    await current_user.save()

    return await gamer_in_round.save()


@router.get('/gamer_in_round/{gamer_in_round_id}', tags=['GamePlayer'])
async def show_round(gamer_in_round_id: str):
    return await GamePlayer.get(gamer_in_round_id)


# ------------- User ------------------------

@router.post("/api/signup", status_code=201, response_model=UserOut, tags=['User'])
async def user_signup(user_data: User):
    user_data.password = get_password_hash(user_data.password)
    return await user_data.save()


@router.post("/token", tags=['User'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}


@router.post("/api/deposit", response_model=UserOut, tags=['User'])
async def get_log(deposit_in: float, current_user: User = Depends(get_current_user)):

    return await update_balance_plus(deposit_in, current_user)
