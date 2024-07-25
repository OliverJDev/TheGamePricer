import requests
from lxml import etree
from games.models import Game
from price.models import *
import threading


def startComparison():
    threads = []
    feeds = [
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=71&affiliate=256", 'da_DK'),
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=50&affiliate=256", 'sv_SE'),
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=51&affiliate=256", 'nb_NO'),
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=70&affiliate=256", 'en_EU'),
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=52&affiliate=256", 'de_DE'),
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=68&affiliate=256", 'en_GB'),
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=59&affiliate=256", 'en_US'),
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=81&affiliate=256", 'en_AU'),
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=82&affiliate=256", 'en_CA'),
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=83&affiliate=256", 'fr_FR'),
        ("https://www.joybuggy.com/module/xmlfeeds/api?id=84&affiliate=256", 'de_CH')
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
            channel = root.find('channel')
            store, created = Store.objects.get_or_create(name='Joy Buggy')

            for element in channel.findall('item', namespaces={'g': 'http://base.google.com/ns/1.0'}):
                title_shop_element = element.find('.//g:title', namespaces={'g': 'http://base.google.com/ns/1.0'})
                if title_shop_element is None:
                    continue
                title_shop = title_shop_element.text

                price_shop_element = element.find('.//g:sale_price', namespaces={'g': 'http://base.google.com/ns/1.0'})
                if price_shop_element is None:
                    continue
                price_shop = price_shop_element.text
                if float(price_shop) >= 99999.99:
                    continue
                link_element = element.find('.//g:link', namespaces={'g': 'http://base.google.com/ns/1.0'})
                if link_element is None:
                    continue
                link = link_element.text

                delivery_time_element = element.find('.//g:delivery_time', namespaces={'g': 'http://base.google.com/ns/1.0'})
                if delivery_time_element is None:
                    continue
                delivery_time = delivery_time_element.text
                if 'out of stock' not in delivery_time:
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
