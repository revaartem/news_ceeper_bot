import json
import os
from datetime import datetime
import telebot
from telebot.apihelper import ApiTelegramException

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
YOUR_CHAT_ID = os.environ.get('YOUR_CHAT_ID')


@bot.message_handler(commands=['start'])
def message_start(message):
    start_message = 'Hello. In this bot you can send to us any information.\n' \
                    'Just type something and push the "Send" button.'
    bot.send_message(message.from_user.id, start_message)


@bot.message_handler(commands=['ban_user'])
def ban_user(message):
    with open('banned_id.json', 'r') as f:
        banned_ids = json.load(f)

    if hasattr(message.reply_to_message, 'forward_from'):
        user_id = message.reply_to_message.forward_from.id
        if user_id in banned_ids:
            bot.send_message(YOUR_CHAT_ID, 'Юзер уже забанен ранее.')
        else:
            banned_ids.append(user_id)
            with open('banned_id.json', 'w') as file:
                json.dump(banned_ids, file)
            bot.send_message(YOUR_CHAT_ID, 'Юзер успешно забанен.')
    else:
        bot.send_message(YOUR_CHAT_ID, "You need to reply with this command to the user's message.")


@bot.message_handler(commands=['unban_user'])
def ban_user(message):
    with open('banned_id.json', 'r') as f:
        banned_ids = json.load(f)

    if hasattr(message.reply_to_message, 'forward_from'):
        user_id = message.reply_to_message.forward_from.id
        if user_id in banned_ids:
            banned_ids.remove(user_id)
            with open('banned_id.json', 'w') as file:
                json.dump(banned_ids, file)
            bot.send_message(YOUR_CHAT_ID, 'Юзер успешно разбанен.')
        else:
            bot.send_message(YOUR_CHAT_ID, 'Юзера нет в списке забаненных аккаунтов.')
    else:
        bot.send_message(YOUR_CHAT_ID, "You need to reply with this command to the user's message.")


@bot.message_handler(commands=['admin_commands'])
def delete_all_from_user(message):
    bot.send_message(message.from_user.id, (message.from_user.id, YOUR_CHAT_ID))
#     if message.from_user.id != YOUR_CHAT_ID:
#         pass
#     else:
#         bot.send_message(YOUR_CHAT_ID, '/ban_user - Ban user (use reply)\n'
#                                        '/unban_user - Unban user (use reply)\n'
#                                        '/clear_history - Clear all messages from user (use reply)')


@bot.message_handler(commands=['clear_history'])
def delete_all_from_user(message):
    with open('messages_id.json', 'r') as f:
        messages_ids = json.load(f)

        if hasattr(message.reply_to_message, 'forward_from') and message.reply_to_message.forward_from is not None:
            user_id = message.reply_to_message.forward_from.id
            for mes_id in messages_ids[str(user_id)]:
                try:
                    bot.delete_message(YOUR_CHAT_ID, mes_id)
                except ApiTelegramException:
                    continue
    try:
        messages_ids[str(user_id)] = []
        with open('messages_id.json', 'w') as file:
            json.dump(messages_ids, file)
    except UnboundLocalError:
        bot.send_message(YOUR_CHAT_ID, 'Use "Reply" to the message from the user you want to delete all others')


@bot.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note",
                                    "voice", "contact", "location", "venue"])
def forward_all_messages(message):
    with open('banned_id.json', 'r') as f:
        banned_ids = json.load(f)

    if message.from_user.id == YOUR_CHAT_ID:
        if hasattr(message.reply_to_message, 'forward_from') and message.reply_to_message.forward_from is not None:
            bot.send_message(message.reply_to_message.forward_from.id, message.text)
        else:
            pass
    else:
        if message.from_user.id in banned_ids:
            bot.send_message(message.from_user.id, "You are banned.")
        else:
            sender_link = f'@{message.from_user.username}'
            message_time = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            sender_hashtag = f'#{message.from_user.username}'

            forward_chat_id = message.chat.id
            forward_message_id = message.message_id

            forwarded_message = bot.forward_message(
                chat_id=YOUR_CHAT_ID,
                from_chat_id=forward_chat_id,
                message_id=forward_message_id
            )

            forward_message = f"Отправитель - {sender_link}\nИстория сообщений - {sender_hashtag}\n" \
                              f"Время отправки к нам - {message_time}"

            message_confirmation = 'Thank you, accepted for processing.'
            forward_to_admin = bot.send_message(YOUR_CHAT_ID, forward_message)
            with open('messages_id.json', 'r') as file:
                messages_ids = json.load(file)
                if str(message.from_user.id) in messages_ids:
                    messages_ids[str(message.from_user.id)].append(forwarded_message.id)
                    messages_ids[str(message.from_user.id)].append(forward_to_admin.id)
                else:
                    messages_ids[message.from_user.id] = [forwarded_message.id, forward_to_admin.id]

                with open('messages_id.json', 'w') as file_w:
                    json.dump(messages_ids, file_w, indent=4)
            bot.send_message(message.from_user.id, message_confirmation)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
