import os
import time
import requests

token = os.getenv("EITAAYAR_TOKEN")
chat_id = os.getenv("CHAT_ID")

if not token:
    raise EnvironmentError("MY_SECRET_TOKEN is not set!")

if not chat_id:
    raise EnvironmentError("CHAT_ID is not set!")

def send_message(text: str) -> dict:
    sent_at: int = int(time.time())
    url = f'https://eitaayar.ir/api/{token}/sendMessage?chat_id={chat_id}&text={text}&title={sent_at=}'
    return requests.get(url).json()

response = send_message('test')
if not response.get('ok'):
    if response.get('description'):
        raise Exception(response.get('description'))
    else:
        raise Exception('something sent wrong!')