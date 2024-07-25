import urllib.request
from lxml import etree
from games.models import Game
from price.models import *
import threading
import xml.etree.ElementTree as ET

def startComparison():
    threads = []
    feeds = [
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=AUS&aff=thegamepricer", 'en_AU'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=BEL&aff=thegamepricer", 'fr_BE'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=BRA&aff=thegamepricer", 'pt_BR'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=CHN&aff=thegamepricer", 'zh_CN'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=DNK&aff=thegamepricer", 'da_DK'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=FIN&aff=thegamepricer", 'fi_FI'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=FRA&aff=thegamepricer", 'fr_FR'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=DEU&aff=thegamepricer", 'de_DE'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=IRL&aff=thegamepricer", 'en_IE'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=ITA&aff=thegamepricer", 'it_IT'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=NLD&aff=thegamepricer", 'nl_NL'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=NOR&aff=thegamepricer", 'nb_NO'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=POL&aff=thegamepricer", 'pl_PL'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=RUS&aff=thegamepricer", 'ru_RU'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=ESP&aff=thegamepricer", 'es_ES'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=SWE&aff=thegamepricer", 'sv_SE'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=CHE&aff=thegamepricer", 'de_CH'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=USA&aff=thegamepricer", 'en_US'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=CAN&aff=thegamepricer", 'en_CA'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=GBR&aff=thegamepricer", 'en_GB'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=TUR&aff=thegamepricer", 'tr_TR'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=JPN&aff=thegamepricer", 'ja_JP'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=KOR&aff=thegamepricer", 'ko_KR'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=IND&aff=thegamepricer", 'en_IN'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=IDN&aff=thegamepricer", 'id_ID'),
        ("https://feeds.gamersgate.com/feeds/thegamepricer?country=THA&aff=thegamepricer", 'th_TH')
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


        with urllib.request.urlopen(url) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        store, created = Store.objects.get_or_create(name='Gamers Gate')


        items_data = []

        for item in root.findall('item'):
            item_data = {}

            for child in item:
                item_data[child.tag] = child.text

            items_data.append(item_data)


        for item in items_data:
            title_shop = item['title']
            if title_shop is None:
                continue

            price_shop = item['price']
            if price_shop is None:
                continue

            if float(price_shop) >= 99999.99:
                continue

            link = item['link']
            if link is None:
                continue

            delivery_time= item['state']
            if delivery_time is None:
                continue

            if delivery_time == 'available':
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

    except urllib.error.URLError as e:
        print(f"Error: Failed to fetch URL - {e}")
    except ET.ParseError as e:
        print(f"Error: Failed to parse XML data - {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")