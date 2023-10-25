from base64 import b64decode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot,types,Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
import openai
import json
import os
from aiogram.dispatcher.filters.state import State,StatesGroup
openai.api_key = ""
model = "gpt-3.5-turbo"
storage=MemoryStorage()
TOKEN = ""

bot=Bot(token=TOKEN)

dp = Dispatcher(bot,storage=storage)

class PR(StatesGroup):
    text=State()

@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.answer("Введите промт:")
    await PR.next()
    await PR.text.set()
@dp.message_handler(state=PR.text)
async def text(message:types.Message,state:FSMContext):
    if message.text=="/start":
        await state.finish()
        await message.answer("Введите промт:")
        await PR.next()
        await PR.text.set()
    else:
        prompt=message.text
        response=openai.Image.create(prompt=prompt,n=1,size="256x256",response_format="b64_json")
        with open("data.json","w") as file:
            json.dump(response,file,indent=4,ensure_ascii=False)
        image_data=b64decode(response["data"][0]["b64_json"])
        file_name="_".join(prompt.split(" "))
        with open(f"{file_name}.png","wb") as file:
            file.write(image_data)
        with open(f"{file_name}.png", "rb") as file:
            await message.answer_photo(file)
            os.remove(f"{file_name}.png")

executor.start_polling(dp,skip_updates=True)



