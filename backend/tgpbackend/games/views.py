import json
import re
import django_filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from games.services.igdb import loadIGDBGame
from games.serializers import *
from games.models import *
from django.http import Http404


class GetAllGameModes(generics.ListCreateAPIView):
    queryset = GameMode.objects.all()
    serializer_class = GameModesSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GameModesSerializer(queryset, many=True)
        return Response(serializer.data)


class GetAllPlayerPerspectives(generics.ListCreateAPIView):
    queryset = PlayerPerspective.objects.all()
    serializer_class = PlayerPerspectiveSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PlayerPerspectiveSerializer(queryset, many=True)
        return Response(serializer.data)


class GetAllThemes(generics.ListCreateAPIView):
    queryset = GameTheme.objects.all()
    serializer_class = GameThemesSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GameThemesSerializer(queryset, many=True)
        return Response(serializer.data)


class GetAllGenres(generics.ListCreateAPIView):
    queryset = GameGenre.objects.all()
    serializer_class = GameGenreSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GameGenreSerializer(queryset, many=True)
        return Response(serializer.data)


class GetAllPlatforms(generics.ListCreateAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PlatformSerializer(queryset, many=True)
        return Response(serializer.data)


class GameFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_name')
    genres = django_filters.CharFilter(method='filter_by_genres')
    platforms = django_filters.CharFilter(method='filter_by_platforms')
    game_modes = django_filters.CharFilter(method='filter_by_game_modes')
    player_perspectives = django_filters.CharFilter(method='filter_by_player_perspectives')
    themes = django_filters.CharFilter(method='filter_by_player_themes')


    def filter_by_name(self, queryset, name, value):
        queryset = queryset.filter(name__contains=value)
        return queryset

    def filter_by_genres(self, queryset, name, value):
        genre_names = value.split(',')
        queryset = queryset
        for genre_name in genre_names:
            queryset = queryset.filter(genres__name=genre_name)
        return queryset

    def filter_by_platforms(self, queryset, name, value):
        genre_names = value.split(',')
        queryset = queryset
        for platform_name in genre_names:
            queryset = queryset.filter(platforms__name=platform_name)
        return queryset

    def filter_by_game_modes(self, queryset, name, value):
        genre_names = value.split(',')
        queryset = queryset
        for game_mode_name in genre_names:
            queryset = queryset.filter(game_modes__name=game_mode_name)
        return queryset

    def filter_by_player_perspectives(self, queryset, name, value):
        genre_names = value.split(',')
        queryset = queryset
        for player_perspective_name in genre_names:
            queryset = queryset.filter(player_perspectives__name=player_perspective_name)
        return queryset

    def filter_by_player_themes(self, queryset, name, value):
        genre_names = value.split(',')
        queryset = queryset
        for theme_name in genre_names:
            queryset = queryset.filter(themes__name=theme_name)
        return queryset

    class Meta:
        model = Game
        fields = ['genres', 'platforms', 'game_modes', 'player_perspectives', 'themes']


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class GetAllGames(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filterset_class = GameFilter
    pagination_class = StandardResultsSetPagination


class GetGameById(APIView):

    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        game = self.get_object(pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)


class GetGameBySlug(APIView):
    def get_object(self, slug):
        try:
            return Game.objects.get(slug=slug)
        except Game.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        game = self.get_object(slug)
        serializer = GameSerializer(game)
        return Response(serializer.data)


class LoadGameById(APIView):
    def get(self, request, *args, **kwargs):
        igdbDataJson = loadIGDBGame(self.kwargs['game'])
        if len(json.loads(igdbDataJson)) == 0:
            return Response('No Game Found ' + str(self.kwargs['game']))

        igdbDataDict = json.loads(igdbDataJson)[0]

        genres = []
        platforms = []
        playerPerspectives = []
        franchises = []
        collections = []
        game_engines = []
        themes = []
        keywords = []
        involved_companies = []
        game_videos = []
        game_modes = []
        websites = []
        cover = 0
        artwork = 0
        screenshot = 0
        header = 0

        # screenshot
        if 'screenshots' in igdbDataDict:
            serializer = ImageSerializer(data=igdbDataDict['screenshots'], many=True)

            if serializer.is_valid():
                for data in serializer.validated_data:
                    Image.objects.update_or_create(id=data['id'], defaults=data)
                    screenshot = data['id']
                    break
            else:
                return Response(serializer.errors)
        # artworks
        if 'artworks' in igdbDataDict:
            serializer = ImageSerializer(data=igdbDataDict['artworks'], many=True)

            if serializer.is_valid():
                for data in serializer.validated_data:
                    Image.objects.update_or_create(id=data['id'], defaults=data)
                    artwork = data['id']
                    break
            else:
                return Response(serializer.errors)
        # websites
        if 'websites' in igdbDataDict:
            serializer = WebsitesSerializer(data=igdbDataDict['websites'], many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    Website.objects.update_or_create(id=data['id'], defaults=data)
                    websites.append(data['id'])
            else:
                return Response(serializer.errors)

        # themes
        if 'themes' in igdbDataDict:
            serializer = GameThemesSerializer(data=igdbDataDict['themes'], many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    GameTheme.objects.update_or_create(id=data['id'], defaults=data)
                    themes.append(data['id'])
            else:
                return Response(serializer.errors)
        # keywords
        if 'keywords' in igdbDataDict:
            serializer = GameKeywordsSerializer(data=igdbDataDict['keywords'], many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    GameKeyword.objects.update_or_create(id=data['id'], defaults=data)
                    keywords.append(data['id'])
            else:
                return Response(serializer.errors)

        # involved companies
        if 'involved_companies' in igdbDataDict:
            serializer = InvolvedCompaniesSerializer(data=igdbDataDict['involved_companies'], many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    Company.objects.update_or_create(id=data['company']['id'], defaults=data['company'])
                    involved_companies.append(data['company']['id'])
            else:
                return Response(serializer.errors)

        # GAME VIDEOS
        if 'videos' in igdbDataDict:
            serializer = GameVideosSerializer(data=igdbDataDict['videos'], many=True)

            if serializer.is_valid():
                for data in serializer.validated_data:
                    GameVideo.objects.update_or_create(id=data['id'], defaults=data)
                    game_videos.append(data['id'])
            else:
                return Response(serializer.errors)

        # GAME MODES
        if 'game_modes' in igdbDataDict:
            serializer = GameModesSerializer(data=igdbDataDict['game_modes'], many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    GameMode.objects.update_or_create(id=data['id'], defaults=data)
                    game_modes.append(data['id'])
            else:
                return Response(serializer.errors)

        # GAME ENGINES
        if 'game_engines' in igdbDataDict:
            serializer = GameEnginesSerializer(data=igdbDataDict['game_engines'], many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    GameEngine.objects.update_or_create(id=data['id'], defaults=data)
                    game_engines.append(data['id'])
            else:
                return Response(serializer.errors)

        # COLLECTIONS
        if 'collections' in igdbDataDict:
            serializer = CollectionsSerializer(data=igdbDataDict['collections'], many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    Collection.objects.update_or_create(id=data['id'], defaults=data)
                    collections.append(data['id'])
            else:
                return Response(serializer.errors)

        # SCREENSHOTS
        if 'franchises' in igdbDataDict:
            serializer = GameFranchisesSerializer(data=igdbDataDict['franchises'], many=True)

            if serializer.is_valid():
                for data in serializer.validated_data:
                    GameFranchise.objects.update_or_create(id=data['id'], defaults=data)
                    franchises.append(data['id'])
            else:
                return Response(serializer.errors)

        # COVER
        if 'cover' in igdbDataDict:
            serializer = ImageSerializer(data=igdbDataDict['cover'], many=False)
            if serializer.is_valid():
                data = serializer.validated_data
                Image.objects.update_or_create(id=data['id'], defaults=data)
                cover = data['id']
            else:
                return Response(serializer.errors)

        # PLAYER PERSPECTIVE
        if 'player_perspectives' in igdbDataDict:
            serializer = PlayerPerspectiveSerializer(data=igdbDataDict['player_perspectives'], many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    PlayerPerspective.objects.update_or_create(id=data['id'], defaults=data)
                    playerPerspectives.append(data['id'])
            else:
                return Response(serializer.errors)

        # PLATFORM
        if 'platforms' in igdbDataDict:
            serializer = PlatformSerializer(data=igdbDataDict['platforms'], many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    Platform.objects.update_or_create(id=data['id'], defaults=data)
                    platforms.append(data['id'])
            else:
                return Response(serializer.errors)

        # GENRE
        if 'genres' in igdbDataDict:
            serializer = GameGenreSerializer(data=igdbDataDict['genres'], many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    GameGenre.objects.update_or_create(id=data['id'], defaults=data)
                    genres.append(data['id'])
            else:
                return Response(serializer.errors)

        # STEAM
        if 'websites' in igdbDataDict:
            filtered_steam = [item for item in igdbDataDict['websites'] if item['category'] == 13]

            if filtered_steam:
                match = re.search(r"/(\d+)$", filtered_steam[0]['url'])
                if match:
                    headerString = str(match.group(1))
                    obj, created = SteamImage.objects.update_or_create(id=filtered_steam[0]['id'],
                                                                       defaults={'image_id': headerString})
                    header = obj.id
                else:
                    # if long url (ie with trailing slash and name)
                    match = re.search(r"/app/(\d+)/", filtered_steam[0]['url'])
                    if match:
                        headerString = str(match.group(1))
                        obj, created = SteamImage.objects.update_or_create(id=filtered_steam[0]['id'],
                                                                           defaults={'image_id': headerString})
                        header = obj.id

        # GAME
        gameSerializer = GameSerializer(data=igdbDataDict)

        if gameSerializer.is_valid():
            gameObj, created = Game.objects.update_or_create(id=gameSerializer.validated_data['id'],
                                                             defaults=gameSerializer.validated_data)
            gameObj.genres.add(*genres)
            gameObj.platforms.add(*platforms)
            gameObj.player_perspectives.add(*playerPerspectives)
            gameObj.franchises.add(*franchises)
            gameObj.collections.add(*collections)
            gameObj.game_engines.add(*game_engines)
            gameObj.game_modes.add(*game_modes)
            gameObj.game_videos.add(*game_videos)
            gameObj.companies.add(*involved_companies)
            gameObj.keywords.add(*keywords)
            gameObj.themes.add(*themes)
            gameObj.websites.add(*websites)
            if cover != 0:
                gameObj.cover = Image.objects.get(id=cover)

            if artwork != 0:
                gameObj.artwork = Image.objects.get(id=artwork)

            if screenshot != 0:
                gameObj.screenshot = Image.objects.get(id=screenshot)

            if header != 0:
                gameObj.header = SteamImage.objects.get(id=header)

            gameObj.save()

            return Response('Downloaded ' + gameObj.name)
        else:
            return Response(gameSerializer.errors)
