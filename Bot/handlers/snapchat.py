from pyrogram import Client, filters
from bs4 import BeautifulSoup
from pyrogram.types import CallbackQuery
import requests

def snapchat(url):
	
	web = "https://www.expertstool.com/converter.php"
	payload = { 
	  "url" : url
	   }
	source = requests.post(web,data=payload).content
	soup = BeautifulSoup(source,"html.parser")
	
	link = soup.find_all("a", {"class" : "btn-primary"})[1]["href"]
	
	if len(link) > 300 or len(link) < 100:
		return {"success": False}
	
	return { "url" : link , "success": True}
# @BENN_DEV & @BENfiles

@Client.on_callback_query(filters.regex(r"^(snapchat)$"))
async def send(client: Client, callback: CallbackQuery):
    user_id = callback.message.from_user.id
    caption = "يمكنك ارسال الرابط الآن."
    answer = await callback.message.chat.ask(text=caption)
    await client.delete_messages(user_id, answer.id)
    await answer.request.edit_text("Processing...")
    url = answer.text
    response = snapchat(url)
    if not response["success"]:
        await answer.request.edit_text("Processing...")
        await answer.reply(
            "الرابط غير صالح",
        )
        return # @BENN_DEV & @BENfiles
    bot = await client.get_me()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    caption = f"● Uploaded By : [{bot_name}]({bot_url})"
    await answer.reply_video(
        video=response["url"],
        caption=caption,
    )
    await answer.request.delete() # @BENN_DEV & @BENfiles