
async def find_a_winner(dragon, tiger):
    """
    functions decides the winner side or tie
    :param dragon: list includes card and its values
    :param tiger: list includes card and its values
    :return: str with the winner card side or tie
    """
    if dragon[1] > tiger[1]:
        return 'dragon'
    if dragon[1] < tiger[1]:
        return 'tiger'
    if dragon[1] == tiger[1]:
        return 'tie'


async def bet_win(dragon_bet, tiger_bet, tie_bet, winner_card):
    """
    functions calculates winners money
    :param dragon_bet: int, player what bet on dragon
    :param tiger_bet: int, player what bet on tiger
    :param tie_bet: int, player what bet on dragon
    :param winner_card: str of winner card
    :return: tuple, with information wining money
    """
    if winner_card == 'dragon':
        return dragon_bet * 1, 0, 0
    if winner_card == 'tiger':
        return 0, tiger_bet * 1, 0
    if winner_card == 'tie':
        return 0, 0, tie_bet * 8
