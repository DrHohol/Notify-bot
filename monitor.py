import asyncio
from time import sleep

from bot import bot
from controller import Controller


async def send_notify():
    while True:
        notifies = Controller.get_active()
        if notifies:
            for notify in notifies:
                await bot.send_message(
                    notify["chat_id"],
                    text=notify["text"],
                    reply_to_message_id=notify["reply_id"],
                )
        sleep(10)


asyncio.run(send_notify())
