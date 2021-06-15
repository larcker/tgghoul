import asyncio
from config import *
from time import sleep
from pyrogram import Client, filters, sync
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions
from pyrogram.types import Message
 
import time
import random

client = Client('ghoul-session', api_id, api_hash)
f = filters.chat([])

limit = 2000

class custom(dict):
    def __missing__(self, key):
        return 0

client.start()

client.stop()

print('Бот запущен')

@client.on_message(f)
def auto_read(_, message: Message):
    app.read_history(message.chat.id)
    message.continue_propagation()


@client.on_message(filters.command("autoscroll", ".") & filters.me)
def add_keep(_, message: Message):
    if message.chat.id in f:
        f.remove(message.chat.id)
        message.edit("Autoscroll deactivated")
    else:
        f.add(message.chat.id)
        message.edit("Autoscroll activated")


@client.on_message(filters.command('ghoul-spam', prefixes=['/', '!', '.']) & filters.me)
def ghoul_handler(client, message):
    i = 1000
    while i > 0:
        try:
            client.send_message(message.chat.id, str(i)+' - 7 = '+str(i-7))
        except FloodWait as e:
            sleep(e.x)

        i -= 7
        sleep(1/messages_per_second)        

    if(end_message != ''):
        client.send_message(message.chat.id, end_message)


@client.on_message(filters.command('spam', prefixes=['/', '!', '.']) & filters.me)
def ghoul_handler(client, message):
    i = 50
    d = "Привееет"
    while i > 0:
        try:
            client.send_message(message.chat.id, str(d))
        except FloodWait as e:
            sleep(e.x)

        i -= 1
        sleep(1/messages_per_second)        

    if(end_message != ''):
        client.send_message(message.chat.id, end_message)


@client.on_message(filters.command('ghoul-c', prefixes=['/', '!', '.']) & filters.me)
def ghoul_handler(client, message):
    i = 1000
    while i > 62:
        try:
            text = f'{i} - 7 = {i-7}'
            for j in range(1,10):
                text += f'\n{i-7*j} - 7 = {i-7*(j+1)}'
            message.edit_text(f'`{text}`')
            sleep(sleep_time_ghoul)
        except FloodWait as e:
            sleep(e.x)

        i -= 7

    if(end_message != ''):
        client.send_message(message.chat.id, end_message)

@client.on_message(filters.command('ghoul', prefixes=['/', '!', '.']) & filters.me)
def ghoul_handler(_, message):
    i = 1000
    while i > 0:
        try:
            message.edit_text(f'{i} - 7 = {i-7}')
        except FloodWait as e:
            sleep(e.x)
        i -= 7    
        sleep(sleep_time)        

    if(end_message != ''):
        message.edit_text(end_message)


@client.on_message(filters.command('words', prefixes=['/', '!', '.']) & filters.me)
def words_handler(client, message):
    words = custom()
    total = 0
    message.delete()
    progress = client.send_message(message.chat.id, '`Загружено 0 сообщений...`')
    for message in client.iter_history(message.chat.id, limit):
        if(message.text):
            splited_text = message.text.split()
        if('Счетчик_слов' not in splited_text):
            total += 1
            if total % 200 == 0:
                progress.edit_text(f'`Загружено {total} сообщений...`')
            for word in splited_text:
                words[word.lower()] += 1

    frequency = sorted(words, key=words.get, reverse=True)
    out = 'Счетчик_слов\n'
    for i in range(10):
        out += f'{i+1}. {frequency[i]} -- {words[frequency[i]]}\n'

    progress.edit_text(out, parse_mode = None)


@client.on_message(filters.command('type', prefixes=['/', '!', '.']) & filters.me)
def type_handler(_, message):
    overriding_text = message.text.split('.type ', maxsplit=1)[1]
    text = overriding_text
    final_message = ''
    typing_symbol = '▒'
 
    while(final_message != overriding_text):
        try:
            message.edit(final_message + typing_symbol)
            sleep(sleep_time)
 
            final_message = final_message + text[0]
            text = text[1:]
 
            message.edit(final_message)
            sleep(sleep_time)
 
        except FloodWait as e:
            sleep(e.x)                    

@client.on_message(filters.command("search", prefixes=['/', '!', '.']) & filters.me)
def search(_, msg):
    perc = 0
 
    while(perc < 100):
        try:
            text = "Поиск самой красивой и лучшей девушки " + str(perc) + "%"
            msg.edit(text)
 
            perc += random.randint(1, 3)
            sleep(0.1)
 
        except FloodWait as e:
            sleep(e.x)
 
    msg.edit("🟢 Девушка успешно найдена!")
    sleep(3)
 
    msg.edit("Выводим результат! ...")
    perc = 0
 
    while(perc < 100):
        try:
            text = "Выводим результат! ..." + str(perc) + "%"
            msg.edit(text)
 
            perc += random.randint(1, 5)
            sleep(0.15)
 
        except FloodWait as e:
            sleep(e.x)
 
    msg.edit("Самая лучшая девушка это Ты! <3 ")
    

@client.on_message(filters.command('music', prefixes=['/', '!', '.']) & filters.me)
async def music_handler(_, message):
    try:
        cmd = message.command

        song_name = ''
        if len(cmd) > 1:
            song_name = ' '.join(cmd[1:])
        elif message.reply_to_message and len(cmd) == 1:
            song_name = (message.reply_to_message.text or message.reply_to_message.caption)
        elif not message.reply_to_message and len(cmd) == 1:
            await message.edit('Напишите имя музыки')
            await asyncio.sleep(2)
            await message.delete()
            return

        song_results = await client.get_inline_bot_results('deezermusicbot', song_name)

        try:
            saved = await client.send_inline_bot_result(
                chat_id='me',
                query_id=song_results.query_id,
                result_id=song_results.results[0].id,
                hide_via=True,
            )

            # Пересылаем сообщение в избранное, как новое
            saved = await client.get_messages('me', int(saved.updates[1].message.id))
            reply_to = (
                message.reply_to_message.message_id
                if message.reply_to_message
                else None
            )
            await client.send_audio(
                chat_id=message.chat.id,
                audio=str(saved.audio.file_id),
                reply_to_message_id=reply_to,
            )

            # Удаляем сообщение из избранного
            await client.delete_messages('me', saved.message_id)
        except TimeoutError:
            await message.edit('Ошибка, пожалуйста, попробуйте позже')
            await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        print(e)
        await message.edit('`Не удалось найти песню`')
        await asyncio.sleep(2)
        await message.delete()


client.run()