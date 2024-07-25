from django.db import models
from games.models import Game


class Currency(models.TextChoices):
    en_GB = 'en_GB',


class Store(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class GamePrice(models.Model):
    currency = models.CharField(max_length=50)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    store = models.ForeignKey(Store, related_name='store', on_delete=models.SET_NULL, blank=True, null=True)
    game = models.ForeignKey(Game, related_name='game', on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    latest = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {} ({})'.format(self.store.name, self.game.name, self.currency)
