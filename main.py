import asyncio
import requests

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.enums import ContentType
import time
import logging

TOKEN = "8756836825:AAHl9MeEcO7s0Zfay8dOi27Pn2pHCzPdCms"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

def location_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Send location", request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_weather(coords):
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        "latitude": coords[0],
        "longitude": coords[1],
        "current_weather": True
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data['current_weather']

@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f"User ID: {user_id} Full Name: {user_full_name} Time: {time.asctime()}")
    await message.answer(
        "Press the button to send your location:",
        reply_markup=location_keyboard()
    )

@dp.message(F.content_type == ContentType.LOCATION)
async def handle_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    coords = [lat, lon]
    weather = get_weather(coords)
    data = {'coordinates': coords, 'temperature': weather['temperature'], 'windspeed': weather['windspeed']}
    await message.answer(
        f"Current weather:\nTemperature: {data['temperature']}\nWindspeed: {data['windspeed']}",
        reply_markup=ReplyKeyboardRemove()
    )


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
