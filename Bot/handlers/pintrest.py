from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
import requests, re

def pintrest(url):
   
   data = {
     "url" : url,
   }
   
   headers = {
      "authority": "pinterestvideodownloader.com",
      "content-type": "application/x-www-form-urlencoded",
    }
  
   response = requests.post("https://pinterestvideodownloader.com/download.php", headers=headers, data=data).text
   result = re.findall(r'<video src="(.*?)"', response)
   match = re.search(r"(.*?)pin(.*?)", url)
   
   if match:
      return {"url": result[0], "success" : True}
   # @BENN_DEV & @BENfiles
   return {"success" : False}
   
@Client.on_callback_query(filters.regex(r"^(pintrest)$"))
async def send(client: Client, callback: CallbackQuery):
    user_id = callback.message.from_user.id
    caption = "يمكنك ارسال الرابط الآن."
    answer = await callback.message.chat.ask(text=caption)
    await client.delete_messages(user_id, answer.id)
    await answer.request.edit_text("Processing...")
    url = answer.text
    response = pintrest(url)
    if not response["success"]:
        await answer.reply(
            "الرابط غير صالح",
        )
        return # @BENN_DEV & @BENfiles
        await answer.request.delete()
    bot = await client.get_me()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    caption = f"● Uploaded By : [{bot_name}]({bot_url})"
    await answer.reply_video(
        video=response["url"],
        caption=caption,
    )
    await answer.request.delete() # @BENN_DEV & @BENfiles