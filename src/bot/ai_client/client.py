import logging
from typing import Dict, Any, Union

from g4f.client import AsyncClient

from src.bot.config import MODEL
from src.bot.logger_setup import setup_logger


logger: logging.Logger = setup_logger()

async def ask_gpt(
    data: Dict[str, Any]
) -> Union[Dict[str, Any], Any]:
    """
    Отправляет данные в GPT-модель и возвращает ответ.

    :param data: Словарь с данными. Может быть:
        - {"type": "text", "content": "строка текста"}
        - {"type": "image", "content": "base64_image", "mime_type": "image/png"}
    :return: Ответ от модели
    """
    client = AsyncClient()
    messages = []

    if data["type"] == "text":
        logger.info("Отправка текстового запроса в модель")
        messages = [
            {
                "role": "user",
                "content": data["content"]
            }
        ]
    elif data["type"] == "image":
        logger.info("Формирование запроса с изображением")
        image_url = f"data:{data['mime_type']};base64,{data['content']}"
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Распознай текст и извлеки анкетные данные с этой фотографии."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ]
    else:
        logger.error(f"Неизвестный тип данных для GPT: {data['type']}")
        raise ValueError("Неизвестный тип данных для GPT")

    logger.info(f"Запрос отправлен. Модель: {MODEL}")

    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        logger.info("Ответ от модели успешно получен")
        return response
    except Exception as e:
        logger.exception("Ошибка при обращении к модели GPT")
        raise