import asyncio
import json
from datetime import datetime

from aiohttp import ClientSession


new_data_list = []
old_data_list = []


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


async def get_and_update_data(secid: str, session, new_data_list):
    while True:
        dict_data = await get_json_data(secid, session)
        new_data_list.append(dict_data[0])
        print(f"new list: {new_data_list}")
        await asyncio.sleep(5)


async def main():
    session = ClientSession()
    secids = ["SBER", "ABIO", "AFLT", "AGRO", "SELG", "TGKA", "VTBR"]
    tasks = []

    for secid in secids:
        task = asyncio.create_task(get_and_update_data(secid, session, new_data_list))
        tasks.append(task)

    while True:
        # print(f"new list: {new_data_list}")
        await asyncio.sleep(5)
        old_data_list = list(new_data_list)
        print(f"old list: {old_data_list}")
        new_data_list.clear()

if __name__ == "__main__":
    new_data_list = []
    old_data_list = []
    asyncio.run(main())
