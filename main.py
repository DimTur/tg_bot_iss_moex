import asyncio
import json
from datetime import datetime

from aiohttp import ClientSession


def get_url(secid: str):
    return f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{secid}/.json?iss.only=marketdata"


async def convert_to_dict(json_data: json, block_name="marketdata"):
    if json_data and block_name in json_data:
        list_of_dicts_securities = [
            {str.lower(column): row[index] for index, column in enumerate(json_data[block_name]["columns"])}
            for row in json_data[block_name]["data"]
        ]
    return list_of_dicts_securities[0]


async def format_data(result):
    formatted_data = []
    for item in result:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        new_dict = {
            "secid": item["secid"],
            "last": item["last"],
            "valtoday": item["valtoday"],
            "systime": formatted_datetime,
        }
        formatted_data.append(new_dict)
    return formatted_data


async def get_json_data(secid: str, session):
    async with session.get(get_url(secid)) as response:
        json_data = await response.json()

    dict_data = await convert_to_dict(json_data)
    formatted_data = await format_data([dict_data])
    return formatted_data


async def main():
    session = ClientSession()
    secids = ["SBER", "ABIO", "AFLT", "AGRO", "SELG", "TGKA", "VTBR"]
    tasks = [get_json_data(secid, session) for secid in secids]
    result = await asyncio.gather(*tasks)
    # print(result)
    new_list = []
    for item in result:
        print(item)
    await session.close()


asyncio.run(main())
