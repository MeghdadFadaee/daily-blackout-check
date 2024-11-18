import os
import time
import requests
from bs4 import BeautifulSoup

token = os.getenv("EITAAYAR_TOKEN")
chat_id = os.getenv("CHAT_ID")

if not token:
    raise EnvironmentError("EITAAYAR_TOKEN is not set!")

if not chat_id:
    raise EnvironmentError("CHAT_ID is not set!")


def send_message(text: str) -> dict:
    sent_at: int = int(time.time())
    url = f'https://eitaayar.ir/api/{token}/sendMessage?chat_id={chat_id}&text={text}&title={sent_at=}'
    return requests.get(url).json()


def get_blockout_page() -> str:
    blockout_link = 'https://qepd.co.ir/fa-IR/DouranPortal/6423'
    blockout_link = 'https://re.rodad.net/blockout'
    return requests.get(blockout_link).text


def make_message(html: str) -> str:
    if len(html) == 0:
        return "خطا در خواندن صفحه!"

    soup = BeautifulSoup(html, 'html.parser')
    # table = soup.find('table', id='ctl01_ctl00_myDataList')

    block_needle = 'بلوك A2'
    paragraphs = soup.find_all('p')
    block = soup.find('p', string=lambda text: isinstance(text, str) and block_needle in text)
    if not block:
        return f"اطلاعات {block_needle} یافت نشد!"

    time_index = paragraphs.index(block) - 1
    return paragraphs[time_index].get_text(separator='\n', strip=True)


def main() -> None:
    try:
        page = get_blockout_page()
        message = make_message(page)
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
