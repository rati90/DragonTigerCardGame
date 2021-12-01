from typing import Optional, List

from beanie import Document


class Game(Document):
    name: str
    min_bet: float
    max_bet: float


class Round(Document):
    game_id: str
    start_time: float
    finish_time: float
    dragon_card: str
    tiger_card: str
    winner: str
    card_left: int
    card_passed: int
    finish: bool


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


