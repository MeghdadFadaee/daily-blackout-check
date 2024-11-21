import os
import re
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


def convert_to_english_numbers(text):
    persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    return text.translate(persian_to_english)


def find_times(text: str) -> list[str]:
	text = convert_to_english_numbers(text)
	pattern = r"(\d{1,2}:\d{2}|\d{1,2})"
	return re.findall(pattern, text)

def is_time_past(time_str: str) -> bool:
    try:
        current_time = datetime.now(iran_tz).time()
        
        if ":" in time_str:
          time_obj = datetime.strptime(time_str.strip(), "%H:%M").time()
        else:
        	time_obj = datetime.strptime(time_str.strip(), "%H").time()
        
        return time_obj < current_time
    except Exception:
        return false

def make_message(html: str) -> str|None:
    if len(html) == 0:
        return "خطا در خواندن صفحه!"

    soup = BeautifulSoup(html, 'html.parser')
    # table = soup.find('table', id='ctl01_ctl00_myDataList')

    block_needle = 'بلوک A4'
    try:
        paragraphs = soup.find_all('p')
        block = soup.find('p', string=lambda text: isinstance(text, str) and block_needle in text)
        time_index = paragraphs.index(block) - 1
        text = paragraphs[time_index].get_text(separator='\n', strip=True)
        start, end, *_ = find_times(text)
        
        if is_time_past(start):
          return None
          
        return text
    except:
        return f"اطلاعات {block_needle} یافت نشد!"


def main() -> None:
    try:
        page = get_blockout_page()
        message = make_message(page)
    except requests.exceptions.Timeout:
        message = 'درخواست ارسال نشد!'
    
    if not message: 
      return None
    
    response = send_message(message)
    if not response.get('ok'):
        if response.get('description'):
            raise Exception(response.get('description'))
        else:
            raise Exception('something sent wrong!')


if __name__ == '__main__':
    main()
