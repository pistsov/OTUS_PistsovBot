from aiohttp import ClientSession
import asyncio

rates_url = 'https://www.cbr-xml-daily.ru/daily_json.js'


async def fetch_json(url: str) -> dict:
    async with ClientSession() as session:
        async with session.get(url) as response:
            data: dict = await response.json(content_type=None)
            return data


async def fetch_eur():
    data = await fetch_json(rates_url)
    eur = data["Valute"]["EUR"]["Value"]
    return eur


async def fetch_usd():
    data = await fetch_json(rates_url)
    usd = data["Valute"]["USD"]["Value"]
    return usd


async def async_main():
    eur, usd = await asyncio.gather(
        fetch_eur(),
        fetch_usd())
    return eur, usd


def main():
    eur, usd = asyncio.run(async_main())
    print(eur, usd)
    return eur, usd


if __name__ == '__main__':
    main()
