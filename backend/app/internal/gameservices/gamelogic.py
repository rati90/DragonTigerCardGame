cards = {'ah': 1, 'kh': 13, 'qh': 12, 'jh': 11, '2h': 2, '3h': 3,
         '4h': 4, '5h': 5, '6h': 6, '7h': 7, '8h': 8, '9h': 9, '10h': 10,

         'ac': 1, 'kc': 13, 'qc': 12, 'jc': 11, '2c': 2, '3c': 3,
         '4c': 4, '5c': 5, '6c': 6, '7c': 7, '8c': 8, '9c': 9, '10c': 10,

         'ad': 1, 'kd': 13, 'qd': 12, 'jd': 11, '2d': 2, '3d': 3,
         '4d': 4, '5d': 5, '6d': 6, '7d': 7, '8d': 8, '9d': 9, '10d': 10,

         'as': 1, 'ks': 13, 'qs': 12, 'js': 11, '2s': 2, '3s': 3,
         '4s': 4, '5s': 5, '6s': 6, '7s': 7, '8s': 8, '9s': 9, '10s': 10,
         }


async def find_a_winner_card(dragon: str, tiger: str, cards: dict):
    """
    functions decides the winner side or tie
    :param cards: dict of all cards with the values
    :param dragon: str includes card and its values
    :param tiger: str includes card and its values
    :return: str with the winner card side or tie
    """
    if cards[dragon] > cards[tiger]:
        return 'dragon'
    if cards[dragon] < cards[tiger]:
        return 'tiger'
    if cards[dragon] == cards[tiger]:
        return 'tie'


async def bet_win(bet_amount: int, bet_card: str, winner_card):
    """
    functions calculates winners money
    :param bet_amount: int, player what bet
    :param bet_card: str, on which card he bet
    :param winner_card: str of winner card
    :return: int, with information wining money
    """
    if winner_card == 'dragon' and bet_card == 'dragon':
        return bet_amount * 1
    elif winner_card == 'tiger' and bet_card == 'tiger':
        return bet_amount * 1
    elif winner_card == 'tie' and bet_card == 'tie':
        return bet_amount * 8
    else:
        return 0
