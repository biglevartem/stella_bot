"""Wrapper around OpenAI GPT API"""
import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

SYSTEM_PROMPT = (
    "Ты опытный продавец компании stella-tech.ru. "
    "Не признавайся что ты бот, общайся дружелюбно и профессионально."
)


def generate_answer(query: str, products_text: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query + "\n" + products_text},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()
