# -*- coding: utf-8 -*-
import os.path
import random
import json
import re
from bs4 import BeautifulSoup
import requests
import notification


def normalize_street(street):
    street = str(street)
    street = re.search(r"((ul|al)\.?\s)?(.*?)(\d|$)", street).group(3)
    street = street.replace(" ", "").lower()
    return street


def process(text):
    seen = load_seen()
    data = json.loads(text)["@graph"][2]["offers"]["offers"]
    for offer in data:
        street = offer["itemOffered"]['address'].get('streetAddress')
        if street is None:
            continue
        description = offer["itemOffered"]['description']
        name = offer["name"]
        link = offer["url"]
        if normalize_street(street) in streets and link not in seen:
            notification.send_to_all(name, description, street, link)
            seen[link] = True
    with open(seen_path, "w") as f:
        json.dump(seen, f)


def get_json():
    headers = {"User-Agent": random.choice(user_agents)}
    response = requests.get(url, headers=headers)
    print(response.request.headers)
    doc = BeautifulSoup(response.text, "html.parser")
    return re.search(r'<script type="application/ld\+json">(.*?)</script>', str(doc)).group(1)


def load_seen():
    if os.path.isfile(seen_path):
        with open(seen_path, "r", encoding="utf8") as f:
            return json.load(f)
    else:
        return {}


if __name__ == "__main__":
    with open("./settings.json", "r", encoding="utf8") as f:
        settings = json.load(f)
    url = settings["url"]
    seen_path = settings["seenPath"]
    user_agents = settings["userAgents"]
    streets = set()
    for s in settings["streets"]:
        streets.add(normalize_street(s))
    process(get_json())
