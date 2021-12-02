from typing import Optional, List
from datetime import datetime
from beanie import Document


class Game(Document):
    name: str
    min_bet: float = 0
    max_bet: float = 0


class Round(Document):
    game_id: str
    finish_time: float = datetime.timestamp(datetime.now()) + 15
    dragon_card: str = None
    tiger_card: str = None
    winner: str = None
    card_passed: int = 0
    finish: bool = False


class GamePlayer(Document):
    game_id: str
    round_id: str
    total_bet: float
    dragon_bet: float
    tiger_bet: float
    tie_bet: float
    money_won: float


class User(Document):
    email: str
    password: str
    deposit: float
    game_history: Optional[List] = []


