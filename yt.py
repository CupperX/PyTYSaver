import asyncio
import yt_dlp
import os
from telebot.async_telebot import AsyncTeleBot
import youthon
from telebot.types import InputFile
import time
import tracemalloc

tracemalloc.start()



Token = "7792678881:AAEd9SnXoIqf9ZCGC5WQSxWPEted4gaMiW4"
#url = input()
bot = AsyncTeleBot(Token)

yt_platform_prefixes = ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/shorts/"]
tt_platform_prefixes = ["https://www.tiktok.com/", "https://vt.tiktok.com/"]

HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }




async def download_video(message):
    url = message.text
    filename = str(f"{time.time()}-{message.from_user.id}.mp4")
    ydl_options = {
            "format": "best",
            "outtmpl": filename,
            "quiet": False,
            "http_headers": HEADERS
            #"extractor_args":{"tiktok": {"webpage_download": True}}
        }
    try:
        with yt_dlp.YoutubeDL(ydl_options) as yt:
               yt.download([url])
               print(filename)
               await bot.send_video(message.chat.id,video=InputFile(filename))
               os.remove(filename)
    except Exception as e:
        print(e)

async def download_yt_video(message):
    url = message.text
    text="Go out"
    if youthon.Video(url).length_seconds > 60:
        bot.reply_to(message,text)
        return
    await download_video(message)

@bot.message_handler(commands=["start"])
async def send_Welcome_Message(message):
    text = "HI"
    bot.reply_to(message,text)

@bot.message_handler(content_types=["text"])
async def check_links(message):
    url = message.text
    for yt_prefix in yt_platform_prefixes:
        if url.startswith(yt_prefix):
            await download_yt_video(message)
            return
    for tt_prefix in tt_platform_prefixes:
        if url.startswith(tt_prefix):
            await download_video(message)
            return
    else:
        bot.reply_to(message,"No")
asyncio.run(bot.polling())