import requests


rates_url = 'https://www.cbr-xml-daily.ru/daily_json.js'


def fetch_json(url: str) -> dict:
    data = requests.get(url).json()
    return data


def fetch_eur():
    data = fetch_json(rates_url)
    eur = data["Valute"]["EUR"]["Value"]
    return eur


def fetch_usd():
    data = fetch_json(rates_url)
    usd = data["Valute"]["USD"]["Value"]
    return usd
