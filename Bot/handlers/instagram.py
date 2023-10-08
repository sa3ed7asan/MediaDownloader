from user_agent import generate_user_agent
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup as Keyboard, InlineKeyboardButton as Button
import requests

# @BENN_DEV & @BENfiles
def instagram(url):
    headers = {
        'authority': 'reelsaver.net',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://reelsaver.net',
        'referer': 'https://reelsaver.net/download-reel-instagram',
        'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': generate_user_agent(),
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
    'via': 'form',
    'ref': 'download-reel-instagram',
    'url': url,}
    response = requests.post('https://reelsaver.net/api/instagram', headers=headers, data=data).json()
    if not response["success"]:
        return { "success" : False }
    user = response['data']['user']['username']
    video = response["data"]['medias'][0]['src']
    urls = { "video" : video, "username" : user , "success" : True}
    return urls

@Client.on_callback_query(filters.regex(r"^(instagram)$"))
async def send(client: Client, callback: CallbackQuery):
    user_id = callback.message.from_user.id
    caption = "يمكنك ارسال الرابط الآن."
    answer = await callback.message.chat.ask(text=caption)
    await client.delete_messages(user_id, answer.id)
    await answer.request.edit_text("Processing...")
    url = answer.text
    response = instagram(url)
    if not response["success"]:
        await answer.request.delete()
        await answer.reply(
            "الرابط غير صالح",
        )
        return # @BENN_DEV & @BENfiles
    bot = await client.get_me ()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    caption = f"● author : [{response['username']}](https://www.instagram.com/{response['username']})\n\n● Uploaded By : [{bot_name}]({bot_url})"
    await answer.reply_video(
        video=response["video"],
        caption=caption,
    )
    await answer.request.delete()
    