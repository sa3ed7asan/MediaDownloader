from pyrogram import Client
import pyromod
# @BENN_DEV & @BENfiles

api_id = 9157919
api_hash = "b90c282e584222babde5f68b5b63ee3b"
bot_token = "6553005927:AAHanAua4_5uqV096BFWDf4Z6HHTcG7qCyo"


app = Client(
    name = "MediaDownloader", 
    api_id = api_id, 
    api_hash = api_hash, 
    bot_token = bot_token,
    in_memory=True, 
    plugins=dict(root="Bot/handlers")
)
