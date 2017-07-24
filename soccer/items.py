# -*- coding: utf-8 -*-

from scrapy import Item, Field


class MatchItem(Item):
    country = Field()
    league = Field()
    date = Field()
    home_team = Field()
    away_team = Field()
    home_goals1 = Field()
    home_goals2 = Field()
    away_goals1 = Field()
    away_goals2 = Field()
