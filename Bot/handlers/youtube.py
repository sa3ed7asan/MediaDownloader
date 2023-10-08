from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup as Keyboard, InlineKeyboardButton as Button
import pytube
from pytube import YouTube

def youtube(url):
    yt = YouTube(url)
    streams = yt.streams
    info = yt.vid_info
    return streams, info["videoDetails"] # @BENN_DEV & @BENfiles
    

def streams_keys(streams, v_id):
    markup = []
    
    for stream in streams:
        if stream.type.startswith(('video', 'audio')):
            res = "🎵" if stream.type.startswith("audio") else stream.resolution
            extension = stream.mime_type.split('/')[-1]
            size = "{:.2f}".format(float(stream.filesize_mb))
            text = f'{res}, {extension}, {size}MB'
            data = f'download {v_id} {stream.itag}'
            markup.append([Button(text, callback_data=data)])
    return markup


@Client.on_callback_query(filters.regex(r"^(youtube)$"))
async def quality(client: Client, callback: CallbackQuery):
    user_id = callback.message.from_user.id
    caption = "يمكنك ارسال الرابط الآن."
    answer = await callback.message.chat.ask(text=caption)
    await client.delete_messages(user_id, answer.id)
    await answer.request.edit_text("Processing...")
    url = answer.text
    try:
        response = youtube(url)
    except pytube.exceptions.RegexMatchError:
        await answer.request.delete()
        await answer.reply(
            "الرابط غير صالح",
        )
        return # @BENN_DEV & @BENfiles
    streams = response[0]
    info = response[1]
    markup = Keyboard(streams_keys(streams, info["videoId"]))
    await answer.request.edit_text(
        "● اختر الجوده المناسبه: ",
        reply_markup=markup
    )

@Client.on_callback_query(filters.regex(r"^(download)"))
async def send(client: Client, callback: CallbackQuery):
    data = callback.data.split()
    response = youtube(f"https://www.youtube.com/watch?v={data[1]}")
    yt = response[0]
    stream = yt.get_by_itag(data[2])
    if not stream:
        client.answer_callback_query("INVALID OR TIMEOUT",  show_alert=True)
        return
    bot = await client.get_me()
    bot_name = bot.first_name
    bot_url = f"{bot.username}.t.me"
    info = response[1]
    title = info["title"]
    length = info["lengthSeconds"]
    views = info["viewCount"]
    thumbnail = info["thumbnail"]["thumbnails"][-1]["url"] # @BENN_DEV & @BENfiles
    caption = f"● Title: {title} \n\n● Duration: {length}sec\n\n● Views: {views}\n\n● Uploaded By : [{bot_name}]({bot_url})"
    if stream.type.startswith(('video', "audio")) and stream.filesize_mb > 100:
        text = "- Content Size Is More Than 50MB. I Can't Upload it to Telegram\n\n" + caption
        markup = Keyboard([
            [
                Button("- Download -", url=stream.url),
                Button("- thumbnail -", url=thumbnail)
            ]
        ])
        await client.edit_message_text(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.id, 
            text=text, 
            reply_markup=markup
        )
        return
    await client.edit_message_text(chat_id = callback.message.chat.id, message_id=callback.message.id, text="Downloading...")
    stream.download()
    await client.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Uploading...")
    await client.send_document(
         chat_id = callback.message.chat.id, 
         document=stream.default_filename,
         caption=caption,# @BENN_DEV & @BENfiles
    )
    await client.delete_messages(callback.message.chat.id , callback.message.id)