from games.models import Game
from price.models import GamePrice
from django.db import transaction
from django.db.models import F, Min


def recalculateAllGames():
    all_game_prices = GamePrice.objects.filter(latest=True).order_by('game', 'price')

    game_price_dict = {}

    for game_price in all_game_prices:
        if game_price.game_id not in game_price_dict:
            game_price_dict[game_price.game_id] = game_price

    with transaction.atomic():
        for game in Game.objects.all():
            if game.id in game_price_dict:
                game.price = game_price_dict[game.id]
            else:
                game.price = None
            game.save()
