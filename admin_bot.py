import requests

# Токен вашего бота
TOKEN = 'YOUR_BOT_TOKEN'
API_URL = f'https://api.telegram.org/bot{TOKEN}/'

# ID администратора
ADMIN_ID = 0

# Получение обновлений
update_id = None


def get_updates(offset=None):
    url = API_URL + 'getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()['result']


# Отправка сообщения
def send_message(chat_id, text):
    url = API_URL + 'sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    requests.post(url, params=params)


print("Бот запущен...")
while True:
    updates = get_updates(update_id)
    for update in updates:
        update_id = update['update_id'] + 1

        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            user_name = message["from"].get("first_name", "Неизвестный")
            text = message.get('text', '')

            if chat_id != ADMIN_ID:
                # Пересылаем сообщение администратору
                send_message(ADMIN_ID, f"Сообщение от пользователя {user_name} ID - {chat_id}: {text}")

                # Подтверждаем получение сообщения пользователю
                send_message(chat_id, "Ваше сообщение отправлено администратору.")
            else:
                if 'reply_to_message' in message:
                    # Если администратор отвечает на пересланное сообщение
                    if ':' in message['reply_to_message']['text']:
                        user_id_text = message['reply_to_message']['text'].split(':')[0]
                        user_id = int(user_id_text.split()[-1].strip())
                        send_message(user_id, f"Ответ от администратора: {text}")
