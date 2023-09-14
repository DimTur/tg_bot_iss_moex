import asyncio
import json

from aiohttp import ClientSession


def get_url(secid: str):
    return f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{secid}/.json?iss.only=marketdata"


async def get_json_data(secid: str, session):
    url = get_url(secid)
    async with session.get(url) as response:
        json_data = await response.json()

    dict_data = await convert_to_dict(json_data)
    return dict_data


async def convert_to_dict(json_data: json, block_name="marketdata"):
    if json_data and block_name in json_data:
        list_of_dicts_securities = [
            {str.lower(column): row[index] for index, column in enumerate(json_data[block_name]["columns"])}
            for row in json_data[block_name]["data"]
        ]
    return list_of_dicts_securities


async def get_shares_by_board_id():
    pass


async def main():
    secids = ["SBER", "ABIO", ]
    async with ClientSession() as session:
        tasks = [get_json_data(secid, session) for secid in secids]
        result = await asyncio.gather(*tasks)
        # print(result)
        for item in result:
            print(item)


asyncio.run(main())
