"""Telegram bot that mirrors the behaviour of the web consultant."""
from __future__ import annotations

import logging
import os
from typing import List

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
  AIORateLimiter,
  Application,
  ApplicationBuilder,
  CommandHandler,
  ContextTypes,
  MessageHandler,
  filters,
)

from .knowledge import ProductKnowledge

logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO,
)
logger = logging.getLogger(__name__)


knowledge = ProductKnowledge.load_default()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text(knowledge.greeting())
  await update.message.reply_text(
    "Напишите, какой эффект вам нужен: энергия, концентрация, спокойный сон или защита иммунитета."
  )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text(
    "Я могу рассказать про ассортимент Felo, составы, вкус, условия доставки и оплату. "
    "Попробуйте спросить, например, 'расскажи про спрей' или 'нужно больше энергии утром'."
  )


def build_responses(user_text: str) -> List[str]:
  responses: List[str] = []
  product = knowledge.find_product(user_text)
  if product:
    responses.append(knowledge.product_details(product))
    faq = knowledge.product_faq(product)
    if faq:
      responses.append(faq)
    responses.append(
      "Если хотите оформить заказ, напишите ваши контактные данные, и менеджер продолжит консультацию."
    )
    return responses

  need = knowledge.detect_need(user_text)
  if need:
    products = knowledge.recommendations(need)
    if products:
      need_messages = {
        "energy": "Для энергии и бодрости подойдут:",
        "focus": "Чтобы держать фокус, присмотритесь к этим позициям:",
        "sleep": "Чтобы расслабиться вечером и лучше спать, советуем:",
        "immunity": "Для поддержки иммунитета доступно:",
      }
      responses.append(need_messages.get(need, "Рекомендации:"))
      responses.extend(knowledge.product_brief(product) for product in products)
      responses.append("Могу рассказать подробнее про любой из продуктов — просто уточните название.")
      return responses

  general = knowledge.general_info(user_text)
  if general:
    responses.extend(general)
    return responses

  lowered = user_text.lower()
  if "ассортимент" in lowered or "список" in lowered:
    responses.append("Актуальные позиции:")
    responses.append(knowledge.product_list())
    responses.append("Напишите название продукта, чтобы получить подробности.")
    return responses

  responses.append(
    "Я могу помочь с выбором продуктов Felo, рассказать про цены, доставку и состав. "
    "Сформулируйте задачу: например, 'нужно просыпаться бодрой утром' или 'какой продукт для иммунитета?'."
  )
  highlights = knowledge.top_highlights()
  if highlights:
    responses.append("Вот наши бестселлеры:")
    responses.extend(highlights)
  return responses


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  if not update.message or not update.message.text:
    return
  user_text = update.message.text.strip()
  if not user_text:
    return

  responses = build_responses(user_text)
  for response in responses:
    await update.message.reply_text(response, parse_mode=ParseMode.HTML)


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text(
    "Извините, я понимаю только текстовые сообщения. Напишите, что хотите узнать про продукты Felo."
  )


def build_application(token: str | None = None) -> Application:
  token = token or os.getenv("TELEGRAM_BOT_TOKEN")
  if not token:
    raise RuntimeError("TELEGRAM_BOT_TOKEN не задан. Установите переменную окружения.")
  return (
    ApplicationBuilder()
    .token(token)
    .rate_limiter(AIORateLimiter())
    .build()
  )


def main() -> None:
  application = build_application()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("help", help_command))
  application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
  application.add_handler(MessageHandler(filters.ALL, fallback))

  logger.info("Bot is polling. Press Ctrl+C to stop.")
  application.run_polling()


if __name__ == "__main__":
  main()
