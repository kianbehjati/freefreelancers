import requests, bs4
from dataclasses import dataclass
from typing import List
import datetime
import dotenv
import os

dotenv.load_dotenv()



API_ADDR = " https://api.producthunt.com/v2/api/graphql"


@dataclass
class BOTMD:
    """
    Best Of The Month Data
    """

    name: str
    description: str
    url: str


def scrape() -> List[BOTMD]:
    """
    return list of top 5 best of the month
    """

    query = """query Getposts($after: DateTime) {posts(first: 5, postedAfter: $after, order: VOTES) {edges {node {name, description, url }}}}"""
    date = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=30)).isoformat() + "Z"
    botmds: List[BOTMD] = []
    response = requests.post(API_ADDR, json={"query": query, "variables": {"after": date}}, headers={"Authorization":f"Bearer {os.getenv('PH_API_KEY')}"})

    for item in response.json()["data"]["posts"]["edges"]:
        node = item["node"]
        botmds.append(BOTMD(name=node["name"], description=node["description"], url=node["url"]))
    return botmds
