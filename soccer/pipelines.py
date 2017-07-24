# -*- coding: utf-8 -*-

import MySQLdb
from datetime import datetime
from scrapy.exceptions import DropItem


class CleaningPipeline(object):
    def process_item(self, item, spider):
        if ("postponed" in item["home_goals1"]) or ("awarded" in item["home_goals1"]) or ("annulled" in item["home_goals1"]):
            raise DropItem("Match was postponed, awarded or annulled...")
        elif (":" not in item["home_goals1"]):
            raise DropItem("No data available")
        else:
            item["league"] = self.clean_league(item["league"])
            item["date"] = self.clean_date(item["date"])
            item["home_team"] = self.clean_home_team(item["home_team"])
            item["away_team"] = self.clean_away_team(item["away_team"])
            item["home_goals1"] = self.clean_home_goals1(item["home_goals1"])
            item["home_goals2"] = self.clean_home_goals2(item["home_goals2"], item["home_goals1"])
            item["away_goals1"] = self.clean_away_goals1(item["away_goals1"])
            item["away_goals2"] = self.clean_away_goals2(item["away_goals2"], item["away_goals1"])
            return item

    def clean_league(self, value):
        return value[value.index(" "):value.index("(")].strip()

    def clean_date(self, value):
        date_str = value[value.index(".") - 2:].strip()
        date = datetime.strptime(date_str, "%d.%m.%Y")
        return date.strftime("%Y-%m-%d")

    def clean_home_team(self, value):
        return value[:value.index(u"—")].strip()

    def clean_away_team(self, value):
        return value[value.index(u"—") + 1:].strip()

    def clean_home_goals1(self, value):
        goals = value[value.index("(") + 1:value.index(")")]
        return int(goals[:goals.index(":")])

    def clean_away_goals1(self, value):
        goals = value[value.index("(")+1:value.index(")")]
        return int(goals[goals.index(":") + 1:])

    def clean_home_goals2(self, value, home_goals1):
        result = value[:value.index("(")]
        home_goals_full = int(result[:result.index(":")].strip())
        return home_goals_full-home_goals1

    def clean_away_goals2(self, value, away_goals1):
        result = value[:value.index("(")]
        away_goals_full = int(result[result.index(":")+1:].strip())
        return away_goals_full - away_goals1


class DatabasePipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(db='soccer_db',
                               user='soccer_user', passwd='soccer_pass',
                               host='0.0.0.0',
                               charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        query = ("INSERT INTO matches (league, country, played, home_team, away_team, home_goals1, "
                 "home_goals2, away_goals1, away_goals2)"
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        self.cursor.execute(query, (item["league"],
                                    item["country"],
                                    item["date"],
                                    item["home_team"],
                                    item["away_team"],
                                    item["home_goals1"],
                                    item["home_goals2"],
                                    item["away_goals1"],
                                    item["away_goals2"],
                                    )
                            )
        self.conn.commit()
        return item