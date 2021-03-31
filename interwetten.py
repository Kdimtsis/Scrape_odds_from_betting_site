from bs4 import BeautifulSoup as bs
import requests
import json
import re

class ApiInterwetten():

    def __init__(self):
        self.name = 'Interwetten'


    def get_odds(self, url):


        r = requests.get(url, "html.parser")
        soup = bs(r.text, "html.parser")

        # RETURNS ALL GAMES IN A LIST
        game = soup.find_all("script", type="application/ld+json")

        odds = []

        for row in game:
            games = str(row)
            date = games.partition("startDate\": \"")[2].split("}")[0].split("T")[0]
            time = games.partition("startDate\": \"")[2].split("}")[0].split("T")[1].replace('\"','')
            Start_date = date + " " + time
            home_team = games.partition("name")[2].split(",")[3].partition("name\": ")[2].split("}")[0]
            away_team = games.partition("awayTeam\": {")[2].split(",")[1].split("name\": ")[1].split("}")[0]

            # URL OF EVERY MATCH
            url_odds = games.partition("url\": ")[2].split(",")[0].split('"')[1]


            #REQUEST THE DATA OF EVERY MATCH
            r2 = requests.get(url_odds, "html.parser")
            soup2 = bs(r2.text, "html.parser")
            words = str(soup2)

            #ALL OFFERS FOR A MATCH
            details = soup2.find_all(class_="offer")


            result = str(details[0])
            home_win = result.split('strong class')[1].split("quote\">")[1].split("<")[0]
            draw = result.split('strong class')[2].split("quote\">")[1].split("<")[0]
            away_win = result.split('strong class')[3].split("quote\">")[1].split("<")[0]

            full_time_result = {
                '1': home_win,
                'X': draw,
                '2': away_win,
            }

            #IN SOME MATCHES THERE IS ONE MORE HANDICAP
            try:
                gg = str(details[7])
                double_chance = str(details[5])
                home_draw = double_chance.split("<span>1X</span>")[1].split("quote\">")[1].split("<")[0]
                home_away = double_chance.split("<span>1X</span>")[1].split("quote\">")[2].split("<")[0]
                away_draw = double_chance.split("<span>1X</span>")[1].split("quote\">")[3].split("<")[0]
                yes_gg = gg.split("<span>Ναι</span>")[1].split("quote\">")[1].split("<")[0]
                no_gg = gg.split("<span>Ναι</span>")[1].split("quote\">")[2].split("<")[0]

            except:
                gg = str(details[6])
                double_chance = str(details[4])
                home_draw = double_chance.split("<span>1X</span>")[1].split("quote\">")[1].split("<")[0]
                home_away = double_chance.split("<span>1X</span>")[1].split("quote\">")[2].split("<")[0]
                away_draw = double_chance.split("<span>1X</span>")[1].split("quote\">")[3].split("<")[0]
                yes_gg = gg.split("<span>Ναι</span>")[1].split("quote\">")[1].split("<")[0]
                no_gg = gg.split("<span>Ναι</span>")[1].split("quote\">")[2].split("<")[0]

            double_chance = {
                        '1X': home_draw,
                        '12': home_away,
                        '2X': away_draw
            }

            both_team_to_score = {
                        'yes':yes_gg,
                        'no':no_gg
                    }

            odds.append({ 'time':Start_date,
                                'home_team':home_team,
                                'away_team':away_team,
                                'full_time_result':full_time_result,
                                'both_teams_to_score':both_team_to_score,
                                'double_chance':double_chance,
                                })

        odds = json.dumps(odds, ensure_ascii=False, indent=2).encode('utf-8')
        odds = odds.decode()
        return odds
























