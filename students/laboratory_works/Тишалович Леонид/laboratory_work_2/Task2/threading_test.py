import threading
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import time


# Настройки базы данных
DATABASE_URL = 'sqlite:///web_scraping.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Определение моделей базы данных
class NewsArticle(Base):
    """
    Модель базы данных для хранения новостных статей.
    """
    __tablename__ = 'news_articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publication_date = Column(DateTime)


class Product(Base):
    """
    Модель базы данных для хранения информации о товарах.
    """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String)
    image_url = Column(String)


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)


def fetch(url):
    """
    Функция для выполнения HTTP-запроса.

    Параметры:
    url (str): URL для запроса.

    Возвращает:
    str: Текст HTML страницы.
    """
    response = requests.get(url)
    return response.text


def parse_news(url):
    """
    Парсинг новостной страницы и сохранение данных в базу данных.

    Параметры:
    url (str): URL страницы для парсинга.
    """
    html = fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h5', class_='card-title').text.strip()
    date_text = soup.find('small', class_='text-muted').text.strip().replace('Опубликовано: ', '')

    try:
        # Попытка парсинга даты публикации
        publication_date = datetime.datetime.strptime(date_text, '%d %B в %H:%M:%S')
    except ValueError:
        # Если формат не совпадает, используем текущее время
        publication_date = datetime.datetime.now()

    db = SessionLocal()
    news_article = NewsArticle(title=title, publication_date=publication_date)
    db.add(news_article)
    db.commit()
    db.close()
    print(f"Сохранена новость: {title}")


def parse_catalog(url):
    """
    Парсинг страницы каталога товаров и сохранение данных в базу данных.

    Параметры:
    url (str): URL страницы для парсинга.
    """
    html = fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    product_cards = soup.find_all('div', class_='card product-card')

    db = SessionLocal()
    for card in product_cards:
        title = card.find('a', class_='no-hover title').text.strip()
        product_url = card.find('a', class_='no-hover')['href']
        image_url = card.find('img', class_='product-img')['src']
        product = Product(title=title, url=product_url, image_url=image_url)
        db.add(product)
    db.commit()
    db.close()
    print(f"Сохранен продукт: {title}")


def main():
    """
    Основная функция для выполнения парсинга.

    Создает потоки для парсинга новостей и каталога товаров и выполняет их параллельно.
    """
    print("Начало выполнения Threading парсинга")
    threads = [
        threading.Thread(target=parse_news, args=('https://parsemachine.com/sandbox/news/',)),
        threading.Thread(target=parse_catalog, args=('https://parsemachine.com/sandbox/catalog/',))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    print("Конец выполнения Threading парсинга")


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Время выполнения threading:", time.time() - start_time)
