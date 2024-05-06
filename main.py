from telethon import TelegramClient, events
import requests
import json

# User data
token = "TokenBotFather" # Token BotFather
token_alldebrid = "TokenApiAlldeBrid" # Token AlldeBrid Premium Account
chat_id = "-100111111111"  # Starts with -100
api_id = 'IdAPI' # Token API ID
api_hash = 'APIHash' # Token API Hash




def send_message_telegram(chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.json()

def transform_url_alldebrid(url):
    api_url = f"https://api.alldebrid.com/v4/link/unlock?agent=python&apikey={token_alldebrid}&link={url}"
    response = requests.get(api_url)
    data = json.loads(response.text)
    if data['status'] == 'success':
        return data['data']['link']
    else:
        return None
    
client = TelegramClient('my_bot', api_id, api_hash).start(bot_token=token)
@client.on(events.NewMessage(chats=int(chat_id)))
async def my_event_handler(event):
    url_transform = ''
    url_pre_transform = event.message.text
    last_message = ''
    
    if url_pre_transform == last_message or url_pre_transform == 'Mensaje no válido' or url_pre_transform.startswith('ENLACES'):
        url_pre_transform = ''
    else:
        result_final = ''
        result_error = ''
        url_split = url_pre_transform.split('\n') # Receive Multiple Links sepparated by a line break
        for url in url_split:
            if url.startswith('https:'):
                try: 
                    url_transform = send_message_telegram(url)
                    if url_transform != None:
                        result_final += url_transform + '\n'
                    else:
                        result_error += url + '\n'
                except:
                    result_error += url + '\n'
            else:
                send_message_telegram(chat_id, 'Invalid Message ⛔') # Send invalid message
        
        #Send Result to Telegram Group
        if result_final and result_error:
            result_total = f'TRANSFORM LINK ✅:\n{result_final}\nLINK ERRORS ⛔:\n{result_error}'
            last_message = result_total

            send_message_telegram(chat_id, result_total)
            
        elif result_final:
            result_total = f'TRANSFORM LINK ✅\n{result_final}\n'
            last_message = result_total

            send_message_telegram(chat_id, result_total)
        elif result_error:
            result_total = f'LINK ERRORS ⛔:\n{result_error}\n'
            last_message = result_total
            send_message_telegram(chat_id, result_total)
            
        #Reset Variables
        result_final = ''
        result_error = ''

client.run_until_disconnected()
