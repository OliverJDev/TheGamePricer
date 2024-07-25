from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from games.models import Game
from price.serializers import GamePriceSerializer
from price.models import GamePrice
from price.stores.gamerecalculation import recalculateAllGames
import importlib

kinguin = importlib.import_module('price.stores.kinguin')
gamersgate = importlib.import_module('price.stores.gamersgate')
gamesplanet = importlib.import_module('price.stores.gamesplanet')
joybuggy = importlib.import_module('price.stores.joybuggy')


class GetAllGamePrices(generics.ListAPIView):
    serializer_class = GamePriceSerializer

    def get_queryset(self):
        game_slug = self.kwargs['game_slug']
        currency = self.kwargs['currency']
        return GamePrice.objects.filter(game__slug=game_slug, latest=True, currency=currency)


class LoadPriceByGameId(APIView):
    def get(self, request, *args, **kwargs):
        gamersgate.startComparison()
        gamesplanet.startComparison()
        joybuggy.startComparison()
        kinguin.startComparison()
        recalculateAllGames()

        return Response("Finished game comparison")
