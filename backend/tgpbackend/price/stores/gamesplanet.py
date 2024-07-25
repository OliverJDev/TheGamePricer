import requests
from lxml import etree
from games.models import Game
from price.models import *
import threading


def startComparison():
    threads = []
    feeds = [
        ("https://fr.gamesplanet.com/api/v1/products/feed.xml?ref=thegamepricer", 'fr_FR'),
        ("https://uk.gamesplanet.com/api/v1/products/feed.xml?ref=thegamepricer", 'en_GB'),
        ("https://de.gamesplanet.com/api/v1/products/feed.xml?ref=thegamepricer", 'de_DE'),
        ("https://us.gamesplanet.com/api/v1/products/feed.xml?ref=thegamepricer", 'en_US'),
    ]

    for feed_url, locale in feeds:
        print(f"Processing feed for {locale} from {feed_url}")
        thread = threading.Thread(target=process_feed, args=(feed_url, locale))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def process_feed(url, currency):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'Upgrade-Insecure-Requests': '1',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            root = etree.fromstring(response.content)

            products = root.findall('.//product')
            store, created = Store.objects.get_or_create(name='Gamesplanet')

            for product in products:
                title_shop = product.findtext('name')
                price_shop = product.findtext('price')
                if float(price_shop) >= 99999.99:
                    continue
                link = product.findtext('link')
                game = Game.objects.filter(name__iexact=title_shop)
                if game.exists():
                    foundGame = game.first()
                    gamePrice = GamePrice.objects.filter(store=store, currency=currency, game=foundGame)
                    if gamePrice.exists():
                        foundGamePrice = gamePrice.latest('timestamp')
                        if float(foundGamePrice.price) != float(price_shop):
                            foundGamePrice.latest = False
                            foundGamePrice.save()
                            GamePrice.objects.create(
                                game=foundGame,
                                store=store,
                                currency=currency,
                                price=price_shop,
                                url=link
                            )
                    else:
                        GamePrice.objects.create(
                            game=foundGame,
                            store=store,
                            currency=currency,
                            price=price_shop,
                            url=link
                        )

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
