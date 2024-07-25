from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from games.models import *
from price.serializers import GamePriceSerializer

class CollectionsSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Collection
        fields = '__all__'



class SteamImageSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = SteamImage
        fields = '__all__'

class ImageSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Image
        fields = '__all__'


class GameFranchisesSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = GameFranchise
        fields = '__all__'


class GameEnginesSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = GameEngine
        fields = '__all__'


class GameThemesSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = GameTheme
        fields = '__all__'


class GameKeywordsSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = GameKeyword
        fields = '__all__'


class WebsitesSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Website
        fields = '__all__'


class CompaniesSerializer(ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Company
        fields = '__all__'


class InvolvedCompaniesSerializer(ModelSerializer):
    company = CompaniesSerializer(many=False, required=True)

    class Meta:
        model = InvolvedCompany
        fields = ['company']


class GameVideosSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = GameVideo
        fields = '__all__'


class GameModesSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = GameMode
        fields = '__all__'


class PlayerPerspectiveSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = PlayerPerspective
        fields = '__all__'


class PlatformSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Platform
        fields = '__all__'


class GameGenreSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = GameGenre
        fields = '__all__'

class GameSerializer(ModelSerializer):
    id = serializers.IntegerField()
    total_rating = serializers.FloatField(source='rating', required=False)
    total_rating_count = serializers.IntegerField(source='rating_count', required=False)
    first_release_date = serializers.CharField(source='release_date', required=False)
    genres = GameGenreSerializer(many=True, read_only=True, required=False)
    player_perspectives = PlayerPerspectiveSerializer(many=True, read_only=True, required=False)
    cover = ImageSerializer(many=False, read_only=True, required=False)
    franchises = GameFranchisesSerializer(many=True, read_only=True, required=False)
    game_engines = GameEnginesSerializer(many=True, read_only=True, required=False)
    collections = CollectionsSerializer(many=True, read_only=True, required=False)
    themes = GameThemesSerializer(many=True, read_only=True, required=False)
    keywords = GameKeywordsSerializer(many=True, read_only=True, required=False)
    involved_companies = InvolvedCompaniesSerializer(many=True, read_only=True, required=False)
    companies = CompaniesSerializer(many=True, read_only=True, required=False)
    videos = GameVideosSerializer(many=True, read_only=True, required=False)
    game_modes = GameModesSerializer(many=True, read_only=True, required=False)
    websites = WebsitesSerializer(many=True, read_only=True, required=False)
    platforms = PlatformSerializer(many=True, read_only=True, required=False)
    artwork = ImageSerializer(many=False, read_only=True, required=False)

    screenshot = ImageSerializer(many=False, read_only=True, required=False)
    header = SteamImageSerializer(many=False, read_only=True, required=False)
    price = GamePriceSerializer(many=False, read_only=True, required=False)


    def validate_first_release_date(self, value):
        return datetime.fromtimestamp(int(value))

    class Meta:
        model = Game
        # fields = '__all__'
        fields = ['id', 'cover', 'videos', 'game_modes', 'involved_companies', 'companies', 'keywords', 'themes', 'collections',
                  'franchises', 'screenshot', 'player_perspectives', 'category', 'status',
                  'total_rating', 'total_rating_count', 'name', 'storyline', 'slug', 'summary',
                  'first_release_date', 'genres', 'game_engines', 'websites', 'platforms', 'artwork', 'header', 'price']
