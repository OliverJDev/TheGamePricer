from rest_framework import serializers
from price.models import GamePrice, Store


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = '__all__'


class GamePriceSerializer(serializers.ModelSerializer):

    store = StoreSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = GamePrice
        fields = '__all__'
