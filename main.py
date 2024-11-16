import os
import time
import requests
from bs4 import BeautifulSoup

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


def get_blockout_page() -> str:
    blockout_link = 'https://qepd.co.ir/fa-IR/DouranPortal/6423'
    return requests.get(blockout_link).text


def main() -> None:
    try:
        page = get_blockout_page()
        soup = BeautifulSoup(page, 'html.parser')
        message = soup.find('table', id='ctl01_ctl00_myDataList').get_text(separator='\n', strip=True)
    except requests.exceptions.Timeout:
        message = 'درخواست ارسال نشد!'

    response = send_message(message)
    if not response.get('ok'):
        if response.get('description'):
            raise Exception(response.get('description'))
        else:
            raise Exception('something sent wrong!')


if __name__ == '__main__':
    main()
