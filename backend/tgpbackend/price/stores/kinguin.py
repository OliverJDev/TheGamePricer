import re

import requests
from lxml import etree
from games.models import Game, Category
from price.models import *
import threading
from fuzzywuzzy import process


def startComparison():
    threads = []
    feeds = [
        ("https://gateway.kinguin.net/feeds/data/google/xml/USD/en?gs=true&countryCode=US", 'en_US'),  # USA (USD)
        ("https://gateway.kinguin.net/feeds/data/google/xml/PLN/pl?gs=true&countryCode=PL", 'pl_PL'),  # Poland (PLN)
        ("https://gateway.kinguin.net/feeds/data/google/xml/EUR/de?gs=true&countryCode=DE", 'de_DE'),  # Germany (EUR)
        ("https://gateway.kinguin.net/feeds/data/google/xml/EUR/fr?gs=true&countryCode=FR", 'fr_FR'),  # France (EUR)
        ("https://gateway.kinguin.net/feeds/data/google/xml/GBP/en?gs=true&countryCode=GB", 'en_GB'),  # UK (GBP)
        ("https://gateway.kinguin.net/feeds/data/google/xml/EUR/it?gs=true&countryCode=IT", 'it_IT'),  # Italy (EUR)
        ("https://gateway.kinguin.net/feeds/data/google/xml/TRY/tr?gs=true&countryCode=TR", 'tr_TR'),  # Turkey (TRY)
        ("https://gateway.kinguin.net/feeds/data/google/xml/CAD/en?gs=true&countryCode=CA", 'en_CA'),  # Canada (CAD)
        ("https://gateway.kinguin.net/feeds/data/google/xml/EUR/es?gs=true&countryCode=ES", 'es_ES'),  # Spain (EUR)
        ("https://gateway.kinguin.net/feeds/data/google/xml/SEK/en?gs=true&countryCode=SE", 'en_SE'),  # Sweden (SEK)
        ("https://gateway.kinguin.net/feeds/data/google/xml/DKK/en?gs=true&countryCode=DK", 'en_DK'),  # Denmark (DKK)
        ("https://gateway.kinguin.net/feeds/data/google/xml/CZK/cz?gs=true&countryCode=CZ", 'cz_CZ'),  # Czech Republic (CZK)
        ("https://gateway.kinguin.net/feeds/data/google/xml/AUD/en?gs=true&countryCode=AU", 'en_AU'),  # Australia (AUD)
        ("https://gateway.kinguin.net/feeds/data/google/xml/CHF/de?gs=true&countryCode=CH", 'de_CH'),  # Switzerland (CHF)
        ("https://gateway.kinguin.net/feeds/data/google/xml/BRL/pt?gs=true&countryCode=BR", 'pt_BR'),  # Brazil (BRL)
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
            'Referer': 'https://www.google.com/',  # Add the referer if needed
            'Upgrade-Insecure-Requests': '1',
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            root = etree.fromstring(response.content)
            channel = root.find('channel')
            store, created = Store.objects.get_or_create(name='Kinguin')
            all_games_title_list = list(Game.objects.values_list('name', flat=True))
            for element in channel.findall('item', namespaces={'g': 'http://base.google.com/ns/1.0'}):
                title_shop_element = element.find('.//title')
                if title_shop_element is None:
                    continue
                title_shop = title_shop_element.text

                price_shop_element = element.find('.//g:price', namespaces={'g': 'http://base.google.com/ns/1.0'})
                if price_shop_element is None:
                    continue
                price_shop = re.sub(r'\b[A-Za-z]+\b|\s', '', price_shop_element.text)

                link_element = element.find('.//link')
                if link_element is None:
                    continue
                link = link_element.text + '?r=66550460cd13c'

                steam_id_element = element.find('.//g:steam_id', namespaces={'g': 'http://base.google.com/ns/1.0'})
                steam_id = steam_id_element.text

                delivery_time_element = element.find('.//g:availability', namespaces={'g': 'http://base.google.com/ns/1.0'})
                if delivery_time_element is None:
                    continue
                delivery_time = delivery_time_element.text

                if delivery_time == 'in stock':
                    game = None
                    if steam_id is not None and steam_id != 'null' and 'dlc' not in title_shop.lower():
                        if '.' not in steam_id and steam_id.isdigit():
                            game = Game.objects.filter(header=steam_id)
                            if game.exists():
                                print('----')
                                print(game)
                    if game is None or len(game) == 0 :
                        for gameCheck in all_games_title_list:
                            if gameCheck.lower() in title_shop.lower():
                                if 'dlc' in title_shop.lower():
                                    game = Game.objects.filter(name=gameCheck, category=Category.DLC_ADDON)
                                else:
                                    game = Game.objects.filter(name=gameCheck, category=Category.MAIN_GAME)

                                if game.exists():
                                    if len(game) != 1:
                                        game_list = list(game.values_list('name', flat=True))
                                        closest_match = process.extractOne(title_shop.lower(), game_list)
                                        print(closest_match)
                                        game = Game.objects.filter(name=closest_match)
                    if game and game.exists():
                        game = game.first()
                        gamePrice = GamePrice.objects.filter(store=store, currency=currency, game=game)

                        if float(price_shop) >= 99999.99:
                            continue
                        if gamePrice.exists():
                            foundGamePrice = gamePrice.latest('timestamp')
                            if float(foundGamePrice.price) != float(price_shop):
                                foundGamePrice.latest = False
                                foundGamePrice.save()
                                GamePrice.objects.create(
                                    game=game,
                                    store=store,
                                    currency=currency,
                                    price=price_shop,
                                    url=link
                                )
                        else:
                            GamePrice.objects.create(
                                game=game,
                                store=store,
                                currency=currency,
                                price=price_shop,
                                url=link
                            )

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
