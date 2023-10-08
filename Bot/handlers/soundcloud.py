from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
import requests

def soundcloud(url):
  params = {
    "url": url
    } 
  response = requests.post("https://api.downloadsound.cloud/track", json=params).json()
  
  mp3 = response['url']
  title = response['title']
  user = response["author"]["username"]
  likes = response["author"]["likes_count"]
  
  return {
    "mp3" : mp3,
    "title" : title,
    "likes" : likes, # @BENN_DEV & @BENfiles
    "username" : user,
  }

@Client.on_callback_query(filters.regex(r"^(soundcloud)$"))
async def send(client: Client, callback: CallbackQuery):
    user_id = callback.message.from_user.id
    caption = "يمكنك ارسال الرابط الآن." # @BENN_DEV & @BENfiles
    answer = await callback.message.chat.ask(text=caption)
    await client.delete_messages(user_id, answer.id)
    await answer.request.edit_text("Processing...")
    url = answer.text
    try:
        response = soundcloud(url)
    except KeyError:
        await answer.request.delete()
        await answer.reply(
            "الرابط غير صالح",
        )
        return
    bot = await client.get_me()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    caption = f"● title : {response['title']}\n● Likes : {response['likes']}\n\n● Uploaded By : [{bot_name}]({bot_url})"
    await answer.reply_audio(
        audio=response["mp3"],
        caption=caption,
    )
    await answer.request.delete() # @BENN_DEV & @BENfiles
    