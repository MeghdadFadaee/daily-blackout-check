import requests
from bs4 import BeautifulSoup


def get_main_page() -> str:
    return requests.get('https://www.qepd.co.ir/').text


def find_blockout_link(html: str) -> None | str:
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a', href=True)
    for a_tag in filter(lambda tag: 'اطلاعات برنامه خاموشی ها' in tag.text, a_tags):
        return a_tag.get('href')
    return None


page = get_main_page()
link = find_blockout_link(page)
if not link:
    raise Exception('unable to find blockout link!')
