import aiohttp
import asyncio
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


async def fetch(session, url):
    """
    Асинхронная функция для выполнения HTTP-запроса.

    Параметры:
    session (aiohttp.ClientSession): Сессия для выполнения запроса.
    url (str): URL для запроса.

    Возвращает:
    str: Текст HTML страницы.
    """
    async with session.get(url) as response:
        return await response.text()


async def parse_news(session, url):
    """
    Парсинг новостной страницы и сохранение данных в базу данных.

    Параметры:
    session (aiohttp.ClientSession): Сессия для выполнения запроса.
    url (str): URL страницы для парсинга.
    """
    html = await fetch(session, url)
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


async def parse_catalog(session, url):
    """
    Парсинг страницы каталога товаров и сохранение данных в базу данных.

    Параметры:
    session (aiohttp.ClientSession): Сессия для выполнения запроса.
    url (str): URL страницы для парсинга.
    """
    html = await fetch(session, url)
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


async def main():
    """
    Основная асинхронная функция для выполнения парсинга.

    Создает задачи для парсинга новостей и каталога товаров и выполняет их параллельно.
    """
    print("Начало выполнения Asyncio парсинга")
    async with aiohttp.ClientSession() as session:
        tasks = [
            parse_news(session, 'https://parsemachine.com/sandbox/news/'),
            parse_catalog(session, 'https://parsemachine.com/sandbox/catalog/')
        ]
        await asyncio.gather(*tasks)
    print("Конец выполнения Asyncio парсинга")


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print("Время выполнения Asyncio:", time.time() - start_time)
