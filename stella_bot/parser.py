"""Simple parser for stella-tech.ru"""
from bs4 import BeautifulSoup
import requests
from .database import Session, Product

CATEGORIES = {
    'yashhiki': 'https://stella-tech.ru/catalog/yashhiki/',
    'kolesa': 'https://stella-tech.ru/catalog/kolesa/',
    'telezhki-gruzovye': 'https://stella-tech.ru/catalog/telezhki-gruzovye/',
    'gidravlicheskie-telezhki': 'https://stella-tech.ru/catalog/gidravlicheskie-telezhki/',
    'verstaki': 'https://stella-tech.ru/catalog/verstaki-i-kozlyi-skladnyie/'
}


def parse_category(name: str, url: str):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    cards = soup.select('.item')
    session = Session()
    for card in cards:
        title = card.select_one('.name').text.strip()
        link = card.select_one('a').get('href')
        article = card.get('data-id', '')
        image = card.select_one('img').get('src', '')
        description = card.select_one('.description')
        description_text = description.text.strip() if description else ''
        product = Product(
            name=title,
            article=article,
            category=name,
            link=link,
            description=description_text,
            image=image
        )
        session.add(product)
    session.commit()
    session.close()


def run():
    for name, url in CATEGORIES.items():
        parse_category(name, url)


if __name__ == '__main__':
    run()
