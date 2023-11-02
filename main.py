# this is a simple telegram bot that uses aiogram library
# it regularly checks my work website for new homeworks to check and
# notifies me about them

import asyncio
import logging
import os
import sys
from typing import List, Tuple
import json

from aiogram import Bot, types
from aiogram import Dispatcher

curl_command = os.environ['CURL_COMMAND']

last_id = None
last_homeworks = None

USER_ID = os.environ['USER_ID']

dp = Dispatcher()


@dp.message()
async def send_last_homeworks(message: types.Message):
    """sends last homeworks"""
    if USER_ID != message.from_user.id:
        return
    global last_id, last_homeworks
    while True:
        while last_homeworks is None or last_homeworks[0][1] == last_id:
            if last_homeworks is not None:
                await asyncio.sleep(60)
            last_homeworks = get_last_homeworks(get_curl_return())
            the_last = last_homeworks[0]

        last_id = the_last[1]
        if the_last[2] or "олимп" in the_last[0].lower():
            reply = f"New homework: {the_last[0]}\n"
            reply += f"{'(to expert check)' if the_last[2] else ''}\n"
            reply += f"Link: https://1.shkolkovo.online/en/admin/homework/users?UserHomework={the_last[1]}\n"
            reply += f"Notion: https://www.notion.so/vsmorodov/60ecefb75cec4aada2e650a7f22eaf47?v=4e4e5228a12a4c0198c2e355dc4b9677&pvs=4\n"
            reply += f"Плюсник: https://docs.google.com/spreadsheets/d/1M00PJN-M-EnRY0s4bWJaaH8TN-lchHddcuUkVMaGeLI/edit"
            await message.answer(reply)


def get_last_homeworks(curl_return: str) -> List[Tuple[str, int, bool]]:
    """parses curl return and returns list of homeworks"""
    curl_return_jsoned = json.loads(curl_return)
    homeworks = curl_return_jsoned['result']
    homeworks = [(homework['HomeworkName'], homework['Id'], homework['ToExpertCheck']) for homework in homeworks]
    return homeworks


def get_curl_return() -> str:
    """returns curl return"""
    return os.popen(curl_command).read()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.environ['BOT_TOKEN'])
    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())
