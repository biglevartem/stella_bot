import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv

from .database import Session, User, Interaction, Tag, init_db
from .utils import search_products, format_products
from .ai import generate_answer

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot = Bot(os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher()

ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x]


async def on_startup():
    init_db()


def add_user(message: Message) -> User:
    session = Session()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        session.add(user)
        session.commit()
    user.last_active = message.date
    session.commit()
    session.close()
    return user


def add_tag(user: User, tag: str):
    session = Session()
    user = session.query(User).filter_by(id=user.id).first()
    tag_obj = session.query(Tag).filter_by(name=tag).first()
    if not tag_obj:
        tag_obj = Tag(name=tag)
    user.tags.append(tag_obj)
    session.commit()
    session.close()


def log_interaction(user: User, text: str):
    session = Session()
    interaction = Interaction(user_id=user.id, text=text)
    session.add(interaction)
    session.commit()
    session.close()


@dp.message(CommandStart())
async def start(message: Message):
    add_user(message)
    await message.answer(
        "Здравствуйте! Чем могу помочь? Задайте вопрос о товарах со stella-tech.ru"
    )


@dp.message(Command("parse"))
async def parse_command(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Команда только для админа")
        return
    from .parser import run
    run()
    await message.answer("Парсинг завершен")


@dp.message()
async def echo(message: Message):
    user = add_user(message)
    query = message.text
    products = search_products(query)
    if products:
        products_text = format_products(products)
        add_tag(user, products[0].category)
    else:
        products_text = ""
    answer = generate_answer(query, products_text)
    await message.answer(answer)
    log_interaction(user, query)


def main():
    asyncio.run(dp.start_polling(bot, on_startup=on_startup))


if __name__ == '__main__':
    main()
