import http.client
import json


def loadIGDBGame(id):
    conn = http.client.HTTPSConnection("api.igdb.com")
    payload = "fields id,name,storyline,slug,total_rating,total_rating_count,summary,first_release_date,status,category," \
              "genres.*,platforms.*,player_perspectives.*, screenshots.*, franchises.*, collections.*, themes.*, keywords.*," \
              "involved_companies.company.*, videos.*, game_modes.*,cover.*, game_engines.*, multiplayer_modes.*, websites.*, artworks.*; where id ={}; ".format(
        id)
    headers = {
        'Client-ID': 'e7gbnyhuli60xm63ir79zdfkrjanlp',
        'Content-Type': 'application/json',
        'Authorization': '',
    }
    conn.request("POST", "/v4/games", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
