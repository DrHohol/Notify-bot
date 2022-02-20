import asyncio
import re
from multiprocessing import Process
from time import sleep

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text

from controller import Controller
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.environ.get('TOKEN'))
dp = Dispatcher()

@dp.channel_post()
async def command_start_handler(message: types.Message) -> None:
    if not message.reply_to_message:
        pass
    else:
        notify_data = await get_data(message)
        print(notify_data)
        if notify_data:
            await message.reply('Notification was set successfully')

            await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
            await asyncio.sleep(3)
            await bot.delete_message(message_id=message.message_id + 1, chat_id=message.chat.id)


async def get_data(message):
    ''' Getting data from message '''
    try:
        date = re.search(r'[^date:]\d+\.\d+\.\d+:.+',
                         message.text).group().strip()
        text = re.search(r'text:.+', message.text).group().split('text:')[1].strip()
        # Not required parameter
        # Will be using in next versions
        try:
            repeats = re.search(
                r'rep:.+', message.text).group().split('rep:')[1]
        except AttributeError:
            repeats = 0
        data = {'text': text, 'time': date, 'repeats': repeats,
                'reply': message.reply_to_message.message_id,
                'chat_id':message.chat.id}
        Controller.create_notify(data)
        return data
    except AttributeError:
        pass


async def send_notify():
    while True:
        notifies = Controller.get_active()
        if notifies:
            for notify in notifies:
                await bot.send_message(notify['chat_id'],
                                       text=notify['text'],
                                       reply_to_message_id=notify['reply_id'])
        sleep(10)

if __name__ == "__main__":

    bot_proc = Process(target=dp.run_polling, args=(bot,))
    bot_proc.start()
    test = Process(target=asyncio.run, args=(send_notify(),))
    test.start()
    # dp.run_polling(bot)
