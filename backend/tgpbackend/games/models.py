from django.db import models
from django_unixdatetimefield import UnixDateTimeField

class WebsiteEnum(models.TextChoices):
    OFFICIAL = 1, ('Official')
    WIKIA = 2, ('Wikia')
    WIKIPEDIA = 3, ('Wikipedia')
    FACEBOOK = 4, ('Facebook')
    TWITTER = 5, ('Twitter')
    TWITCH = 6, ('Twitch')
    INSTAGRAM = 8, ('Instagram')
    YOUTUBE = 9, ('Youtube')
    IPHONE = 10, ('IPhone')
    IPAD = 11, ('IPad')
    ANDROID = 12, ('Android')
    STEAM = 13, ('Steam')
    REDDIT = 14, ('Reddit')
    ITCH = 15, ('Itch')
    EPICGAMES = 16, ('Epic Games')
    GOG = 17, ('GOG')
    DISCORD = 18, ('Discord')
    def label_by_type_value(value):
        choices = [c[1] for c in WebsiteEnum.choices if c[0] == value]
        return choices[0] if len(choices) else None


class Website(models.Model):
    category = models.CharField(
        max_length=30,
        choices=WebsiteEnum.choices,
        default=WebsiteEnum.OFFICIAL,
    )
    trusted = models.BooleanField(default=True)
    url = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return WebsiteEnum.label_by_type_value(self.category)


#igdb image (need for id)
class Image(models.Model):
    image_id = models.CharField(max_length=100, blank=True)
    height = models.IntegerField(blank=True)
    width = models.IntegerField(blank=True)
    animated = models.BooleanField(default=False)

    def __str__(self):
        return self.image_id

class SteamImage(models.Model):
    image_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.image_id

class Collection(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class GameEngine(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class GameVideo(models.Model):
    name = models.CharField(max_length=100, blank=True)
    video_id = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name


class GameTheme(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class GameFranchise(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class GameKeyword(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.slug


class InvolvedCompany(models.Model):
    company = models.ForeignKey(Company, related_name='company', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.slug


class GameMode(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class GameGenre(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class PlayerPerspective(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=100, blank=True)
    abbreviation = models.CharField(max_length=50, blank=True)
    alternative_name = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Category(models.TextChoices):
    MAIN_GAME = 0, ('Main Game')
    DLC_ADDON = 1, ('DLC Addon')
    EXPANSION = 2, ('Expansion')
    BUNDLE = 3, ('Bundle')
    STANDALONE_EXPANSION = 4, ('Standalone Expansion')
    MOD = 5, ('Mod')
    EPISODE = 6, ('Episode')
    SEASON = 7, ('Season')
    REMAKE = 8, ('Remake')
    REMASTER = 9, ('Remaster')
    EXPANDED_GAME = 10, ('Expanded Game')
    PORT = 11, ('Port')
    FORK = 12, ('Fork')
    PACK = 13, ('Pack')
    UPDATE = 14, ('Update')


class Status(models.TextChoices):
    RELEASED = 0, ('Released')
    ALPHA = 2, ('Alpha')
    BETA = 3, ('Beta')
    EARLY_ACCESS = 4, ('Early Access')
    OFFLINE = 5, ('Offline')
    CANCELLED = 6, ('Cancelled')
    RUMORED = 7, ('Rumored')
    DELISTED = 8, ('Delisted')


class Game(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    release_date = UnixDateTimeField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    storyline = models.TextField(blank=True, null=True)
    platforms = models.ManyToManyField(Platform, blank=True)
    player_perspectives = models.ManyToManyField(PlayerPerspective, blank=True)
    genres = models.ManyToManyField(GameGenre, blank=True)
    game_modes = models.ManyToManyField(GameMode, blank=True)
    game_videos = models.ManyToManyField(GameVideo, blank=True)
    companies = models.ManyToManyField(Company, blank=True)
    keywords = models.ManyToManyField(GameKeyword, blank=True)
    themes = models.ManyToManyField(GameTheme, blank=True)
    game_engines = models.ManyToManyField(GameEngine, blank=True)
    collections = models.ManyToManyField(Collection, blank=True)
    franchises = models.ManyToManyField(GameFranchise, blank=True)
    websites = models.ManyToManyField(Website, blank=True)

    cover = models.ForeignKey(Image, related_name='cover', on_delete=models.CASCADE, blank=True, null=True)
    screenshot = models.ForeignKey(Image, related_name='screenshot', on_delete=models.CASCADE, blank=True, null=True)
    artwork = models.ForeignKey(Image, related_name='artwork', on_delete=models.CASCADE, blank=True, null=True)
    header = models.ForeignKey(SteamImage, related_name='header', on_delete=models.CASCADE, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RELEASED,
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.MAIN_GAME,
    )

    price = models.ForeignKey('price.GamePrice', related_name='best_price', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
