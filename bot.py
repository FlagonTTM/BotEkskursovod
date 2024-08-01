from aiogram.utils.executor import start_polling
from config import TOKEN
from aiogram.types.message import ContentType, Message
from keyboard import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram import Bot, Dispatcher, types
from db import *
import requests

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
user_data = {}

def add_message_to_user_data(user_id, message_id):
    if user_id in user_data:
        user_data[user_id].append(message_id)
    else:
        user_data[user_id] = [message_id]

def check_premium(user_id):
    return is_premium(user_id)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, a=None):
    add_user(message.from_user.id, message.from_user.username)
    sent_message = await message.answer_photo(
        photo='https://i.postimg.cc/kgCdZ8d4/2024-08-01-151919786.png', reply_markup=keyboard)
    sent_message1 = await message.answer('Привет, я сурок Стёпа, и сегодня я проведу тебе одну из экскурсий!')
    sent_message2 = await message.answer('Ответишь на пару вопросов, чтобы я смог выбрать для тебя маршрут'
                         ' или хочешь сам?', reply_markup=start)

@dp.message_handler(lambda message: message.text == 'Вернуться в меню')
async def go_back_to_menu(message: types.Message):
    await message.answer_photo(
        photo='https://i.postimg.cc/kgCdZ8d4/2024-08-01-151919786.png')
    await message.answer('Привет, я сурок Стёпа, и сегодня я проведу тебе одну из экскурсий!')
    await message.answer('Ответишь на пару вопросов, чтобы я смог выбрать для тебя маршрут'
                         ' или хочешь сам?', reply_markup=start)

@dp.message_handler(lambda message: message.text == 'Платная подписка')
async def sub(message: types.Message):
    if message.chat.id in user_data:
        for message_id in user_data[message.chat.id]:
            await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
        user_data[message.chat.id] = []
    sent_message = await message.answer('Для получения доступа к нейросети по достопримечательностям Междуреченска,'
                         ' а также к дополнительным экскурсиям приобрети платную подписку', reply_markup=podpiska)
    add_message_to_user_data(message.chat.id, sent_message.message_id)

@dp.message_handler(lambda message: message.text == 'Платное меню')
async def go_back_to_menu(message: types.Message):
    if check_premium(message.from_user.id):
        await message.answer_photo(
            photo='https://i.postimg.cc/kgCdZ8d4/2024-08-01-151919786.png', reply_markup=gold)
        await message.answer('Привет, я сурок Стёпа, и сегодня я проведу тебе одну из экскурсий!')
        await message.answer('Ответишь на пару вопросов, чтобы я смог выбрать для тебя маршрут'
                             ' или хочешь сам?', reply_markup=gold_start)
    else:
        await message.answer('У тебя не оформлена подписка', reply_markup=exc1_menu)

# Подключение к YandexGPT
api_key = 'AQVN0wc2GBoLHdJMLBGJR1OYZmRpyBJ-szmZ5Bnu'

@dp.message_handler()
async def reply_to_other_messages(message: types.Message):
    if check_premium(message.from_user.id):
        msg = message.text
        if msg != 'Вернуться в меню' and msg != 'Платная подписка' and msg != 'Платное меню':
            resp = requests.post(
                url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                headers = {
                    "x-folder-id": "b1gic2i3ehuar676m62p",
                    "Authorization": f"API-KEY {api_key}"
                },
                json = {
                    "modelUri": "gpt://b1gic2i3ehuar676m62p/yandexgpt-lite/latest",
                    "completionOptions": {
                        "stream": False,
                        "temperature": 0.6,
                        "maxTokens": "100"
                    },
                    "messages": [
                    {
                      "role": "system",
                      "text": "Рассказ про достопримечательности города Междуреченск Кемеровской области, отвечать на вопрос в 30-40 слов, не говори местоположение объекта"
                    },
                    {
                      "role": "user",
                      "text": msg
                    }
                ]

                }
            )
            answer = resp.json()
            reply_txt = answer['result']['alternatives'][0]['message']['text']
            await message.answer(reply_txt)

@dp.callback_query_handler(text='exc1_menu')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    sent_message = await bot.send_photo(call.message.chat.id,
        photo='https://i.postimg.cc/kgCdZ8d4/2024-08-01-151919786.png', reply_markup=keyboard)
    sent_message1 = await bot.send_message(call.message.chat.id,'Привет, я сурок Стёпа, и сегодня я проведу тебе одну из экскурсий!')
    sent_message2 = await bot.send_message(call.message.chat.id,'Ответишь на пару вопросов, чтобы я смог выбрать для тебя маршрут'
                         ' или хочешь сам?', reply_markup=start)

    add_message_to_user_data(call.message.chat.id, sent_message.message_id)
    add_message_to_user_data(call.message.chat.id, sent_message1.message_id)
    add_message_to_user_data(call.message.chat.id, sent_message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='subscribe')
async def subscribe(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    set_premium(call.from_user.id, 1)
    sent_message = await bot.send_message(call.from_user.id, 'Спасибо за оформление подписки! Теперь у вас есть доступ к эксклюзивным экскурсиям.', reply_markup=gold_menu)
    add_message_to_user_data(call.message.chat.id, sent_message.message_id)
    await call.answer()


@dp.callback_query_handler(text='unsubscribe')
async def unsubscribe(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    set_premium(call.from_user.id, 0)
    sent_message = await bot.send_message(call.from_user.id, 'Ваша подписка отменена', reply_markup=exc1_menu)
    add_message_to_user_data(call.message.chat.id, sent_message.message_id)
    await call.answer()


@dp.callback_query_handler(text='menu')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    sent_message = await bot.send_message(call.message.chat.id,'Привет! Спасибо, что прошёл одну из наших экскурсий! Как будет время пройди и остальные!', reply_markup=exc_var)

    add_message_to_user_data(call.message.chat.id, sent_message.message_id)
    await call.answer()

@dp.callback_query_handler(lambda c: c.data == 'sam')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'У нас есть 4 экскурсии, 2 в разных районах и 2 с подъемом на гору!', reply_markup=exc_var)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(lambda c: c.data == 'ne_sam')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, "Где ты предпочтешь проводить свободно время:\nВ спортзале или в музее", reply_markup=start_var)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='start_var2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []

    message = await bot.send_message(call.message.chat.id, 'А теперь второй вопрос')
    message1 = await bot.send_message(call.message.chat.id, 'Если ты поедешь отдыхать с друзьями, что выберешь путешествие зимой или летом?', reply_markup=queue)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='summer')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []

    message = await bot.send_message(call.message.chat.id, 'И последний вопрос')
    message1 = await bot.send_message(call.message.chat.id, 'Хочешь ли ты легкую прогулку по городу или с подъемом на гору "Сыркашинская"?', reply_markup=longorshort)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()


@dp.callback_query_handler(text='big_in_priroda')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []

    message = await bot.send_message(call.message.chat.id, 'Начинаем нашу экскурсию! Высылаю точку')
    message1 = await bot.send_message(call.message.chat.id, 'https://yandex.ru/maps/-/CCU6ESQ9cA')
    message2 =await bot.send_message(call.message.chat.id, 'Как дойдёшь до точки, дай мне знать!', reply_markup=exc1_point0)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='mesto-1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []

    message = await bot.send_photo(call.message.chat.id, photo='https://i.postimg.cc/qBCxmBHb/2024-08-01-161727971.png')
    message1 = await bot.send_message(call.message.chat.id, 'Если ты посмотришь на Юг - то увидишь наш вокзал')
    message2 = await bot.send_message(call.message.chat.id, 'А вот немного информации про него:')
    message3 = await bot.send_message(call.message.chat.id, 'Железнодорожный вокзал - одно из мест, через которое можно приехать в Междуреченск. '
                                  'Был открыт в 1959 году. Трижды за свою историю вокзал реконструировался и расширялся. ')
    message4 = await bot.send_message(call.message.chat.id, 'Начнём идти до следующей точки. Дойди до заправки ГазПром. Рядом ты видишь частные дома. Это район "Нахаловка" ')
    message5 = await bot.send_message(call.message.chat.id, 'Иди по тропинке ул. Доватора вдоль района до смотровой площадки дамбы.'
                                  ' Как только доберешься до смотровой площадки, дай знать!',
                                  reply_markup=exc1_point1)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point-1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Перед тобой река Уса. Каждое лето люди любят в ней купаться и отдыхать на ее берегах. '
                                  'Как ты думаешь, какова протяженность реки?', reply_markup=exc1_ans1)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_false_ans1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'❌К сожалению, неправильно❌', reply_markup=exc1_again_ans1)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_true_ans1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'✅Молодец! Ты угадал!✅')
    message1 = await bot.send_photo(call.message.chat.id,
        photo='https://i.postimg.cc/WbG6v930/2024-08-01-161754697.png')
    message2 = await bot.send_message(call.message.chat.id,
        'Как только насладишься видом на реку и гору, начинай свое приключение по дамбе направо (против течения реки).'
        ' Наслаждайся видами, пока не дойдешь до лысой горы.'
        'Ты узнаешь её из тысячи)', reply_markup=exc1_point2)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point-2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,
        'Думаю ты уже догадался, почему это гора называется "Лысая", на её вершине большая плешь.')
    message1 = await bot.send_message(call.message.chat.id,'По одной из версий, она образовалась более полувека назад. '
                                  'Тогда для того, чтобы осушить болото (на котором и стоит Междуреченск по сей день) и уплотнить грунт,'
                                  'строительные бригады на "Лысой" горе добывали бутовый камень.',
                                  reply_markup=exc1_point3)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point-3')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'А теперь дойди до этого моста!')
    message1 = await bot.send_photo(call.message.chat.id,
        photo='https://i.postimg.cc/wj95ThyZ/2024-08-01-161830472.png')
    message2 = await bot.send_message(call.message.chat.id,'Как думаешь, когда его построили?', reply_markup=exc1_ans2)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_false_ans2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'❌Упс, ошибочка!❌', reply_markup=exc1_again_ans2)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_true_ans2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'✅Ура! Это верный ответ!✅')
    message1 = await bot.send_message(call.message.chat.id,'Его построили в 1952 году для соединения города и промзоны.')
    message2 = await bot.send_message(call.message.chat.id,
        'Теперь поворачивай направо и иди до пешеходного перехода, после этого поверни и ступай к началу '
        '"Аллеи сказок". Как дойдёшь, нажми на кнопку!', reply_markup=exc1_point4)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point4')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,
        'Иди прямо по аллее до памятника ликвидаторам аварии на Чернобыльской АЭС, а пока я расскажу о нём')
    message1 = await bot.send_photo(call.message.chat.id,
        photo='https://i.postimg.cc/6pzr7yC3/2024-08-01-161859104.png')
    message2 = await bot.send_message(call.message.chat.id,'Этот памятный знак - символ подвига и жертв тысяч наших соотечественников – '
                                  'ликвидаторов Чернобыльской и других радиационных аварий.'
                                  ' Памятник был установлен в 2017 году по инициативе общественной организации Союз «Чернобыль».',
                                  reply_markup=exc1_point5)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point5')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'Шагай дальше по аллее. Ты увидишь сказочных персонажей: грибы-гномы и колобок.'
                            ' Как только дойдешь до репки, оповести меня!')
    message1 = await bot.send_photo(call.message.chat.id,
        photo='https://i.postimg.cc/g0Jv3mKK/2024-08-01-161920860.png',
        reply_markup=exc1_point6)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point6')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'Напомни, как называется сказка, в которой герои были репка и медведь?', reply_markup=exc1_ans3)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_false_ans3')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'❌Ой! Подумай ещё раз!❌', reply_markup=exc1_again_ans3)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_true_ans3')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'✅Да! Правильно!✅')
    message1 = await bot.send_message(call.message.chat.id,'Тогда дедка смог перехитрить мишку и отдать ему вершки репы и корешки пшеницы')
    message2 = await bot.send_message(call.message.chat.id,'Иди дальше вдоль аллеи, пока не дойдешь до выхода из нее. \n'
                                  'Как только будешь на месте, скажешь мне!', reply_markup=exc1_point7)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point7')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/GtkYb2cb/2024-08-01-162021533.png')
    message = await bot.send_message(call.message.chat.id,'Посмотри на выход, как думаешь, какая сказка на нём изображена?', reply_markup=exc1_ans4)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_false_ans4')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'❌Попробуй ответить по другому!❌', reply_markup=exc1_again_ans4)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_true_ans4')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'✅Всё верно!✅')
    message1 = await bot.send_message(call.message.chat.id,
        'У лукоморья дуб зелёный;\n Златая цепь на дубе том:\n И днём и ночью кот учёный\n Всё ходит по цепи кругом;')
    message2 = await bot.send_message(call.message.chat.id,'Выход олицетворяет именно эти строчки!')
    message3 = await bot.send_message(call.message.chat.id,'Ты побывал в сказке! Теперь можно двигаться дальше!')
    message4 = await bot.send_message(call.message.chat.id,'Обойди ледовый дворец "Кристалл" с правой стороны, которая ближе к дороге.')
    message5 = await bot.send_photo(call.message.chat.id,
        photo='https://imgur.com/a/0o5nmSo')
    message6 = await bot.send_message(call.message.chat.id,'Как дойдёшь до кинотеатра "Кузбасс", оповести меня!', reply_markup=exc1_point8)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point8')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'Как думаешь, в каком году был построен кинотеатр "Кузбасс"?', reply_markup=exc1_ans5)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_false_ans5')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'❌Не верно, но тебя есть ещё шансы!❌', reply_markup=exc1_again_ans5)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_true_ans5')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'✅Прямо в точку!✅')
    message1 = await bot.send_photo(call.message.chat.id,
        photo='https://i.postimg.cc/8C9rWWc1/2024-08-01-162329377.png')
    message2 = await bot.send_message(call.message.chat.id,
        'Кинотеатр "Кузбасс", построен в 1956г. и открыт 31 декабря, как новогодний подарок жителям города.')
    message3 = await bot.send_message(call.message.chat.id,'Обновлённый кинотеатр "Кузбасс" открылся после реконструкции в 2003 году и'
                                  ' так же стал одним из любимых мест проведения досуга жителей города.')
    message4 = await bot.send_photo(call.message.chat.id,
        photo='https://i.postimg.cc/sXPDXZZH/2024-08-01-162837137.png')
    message5 = await bot.send_message(call.message.chat.id,
        'После кинотеатра расположен городской парк, где летом дети и взрослые любят весело проводить время. '
        'В нем находится Гулливер - один из символов города Междуреченска')
    message6 = await bot.send_message(call.message.chat.id,'Как только прогуляешься по парку и найдешь Гулливера, скажешь мне',
                                  reply_markup=exc1_point9)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point9')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'Посмотри какой он большой!')
    message1 = await bot.send_message(call.message.chat.id,'Говорят, если обойти его обе ноги в форме знака "бесконечность" 3 раза,'
                                  ' и при этом загадывать желание, то оно обязательно сбудется.')
    message2 = await bot.send_message(call.message.chat.id,'Справа от Гулливера находится карусель "Вихрь", а рядом с ней тропа,'
                                  '  вдоль которой растут высокие и густые ели. Иди по ней, пока не дойдешь до Монумента Славы!',
                                  reply_markup=exc1_point10)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point10')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'Автор мемориала – Владимир Борисович Смирнов. Монумент был открыт в 1981 году.')
    message1 = await bot.send_message(call.message.chat.id,
        ' Первый фрагмент символизирует начало войны, на нем изображено прощание сына-воина с матерью. ')
    message2 = await bot.send_message(call.message.chat.id,
        'На центральной части композиции в центре расположен барельеф солдата, слева от него собирательный портрет партизана,'
        ' справа – труженицы-женщины.')
    message3 = await bot.send_message(call.message.chat.id,
        'Позади стелы слева и справа симметрично расположены железобетонные стены, на которых выбиты имена погибших'
        ' людей, жившие в Междуреченском городском округе')
    message4 = await bot.send_message(call.message.chat.id,
        'С боковых сторон их украшают отлитые в бетоне знамена. На левой стене – рельефная надпись'
        ' – четверостишье поэта Роберта Рождественского:'
        ' «Вспомним всех поименно…».')
    message5 = await bot.send_photo(call.message.chat.id,
        photo='https://i.postimg.cc/fyBz7nCx/2024-08-01-162925035.png')
    message6 = await bot.send_message(call.message.chat.id,'Прямо за монументом есть тропа, которая ведет обратно на дамбу, '
                                  'но чтобы выйти на неё, нужно пройти под подъемом лыжероллерной трассы. Как подойдешь к ней, дай знать!',
                                  reply_markup=exc1_point11)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point11')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'Протяжённость этой трассы 1050 метров, с двумя арками-подъемами и современным покрытием — подарок жителям города от семьи В.В. Мельниченко.')
    message1 = await bot.send_message(call.message.chat.id,'Теперь поднимайся на дамбу и продолжай свой путь, пока не увидишь с правой стороны частные дома. \n Как увидишь, скажешь мне!', reply_markup=exc1_point12)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_point12')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'Как думаешь, в каком ты сейчас районе находишься?', reply_markup=exc1_ans6)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_false_ans6')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'❌К сожалению, неправильно❌', reply_markup=exc1_again_ans6)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_true_ans6')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id,'✅Ты полностью прав!✅')
    message1 = await bot.send_message(call.message.chat.id,'Старое Междуречье - один из первых районов Междуреченска')
    message2 = await bot.send_message(call.message.chat.id,'Теперь иди до конца дамбы, пока не дойдешь до Церкви.')
    message3 = await bot.send_photo(call.message.chat.id,photo='https://i.postimg.cc/Rhsm61Cd/2024-08-01-163016337.png')
    message4 = await bot.send_message(call.message.chat.id,'На этом мы подходим к концу, но можем продолжить поднятием на Сыркашинскую', reply_markup=menu)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    await call.answer()

@dp.callback_query_handler(text='gora')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Выбери маршрут', reply_markup=puti)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_extreme')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message0 = await bot.send_message(call.message.chat.id, 'https://yandex.ru/maps/-/CDWhu84a')
    message = await bot.send_message(call.message.chat.id, 'Ты выбрал экстремальный маршрут, хороший выбор) \n Тебе нужно обойти церковь через диспетчер'
                                  'скую станцию, перейти дорогу, и подняться вверх в гору через деревню Сыркаши.'
                                  ' \n Первое, что ты пройдешь, будет пиццерия «Радора», затем небольшой поворот направо, затем налево и прямо до конца, по'
                                  'ка не выйдешь на большую поляну. Когда все дома будут позади тебя, ты увидишь крутой подъем на гору'
                                  ' прямо перед собой, вот туда тебе нужно подняться. Проверь на что ты способен! \n Как только поднимешься, скажешь мне!')
    message1 = await bot.send_message(call.message.chat.id, 'Вот тебе карта с маршрутом, чтобы ты точно не потерялся)')
    message2 = await bot.send_photo(call.message.chat.id,
                                    photo='https://imgur.com/a/0TISTfH', reply_markup=exc1_extreme)
    add_message_to_user_data(call.message.chat.id, message0.message_id)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_calm')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message0 = await bot.send_message(call.message.chat.id, 'https://yandex.ru/maps/-/CDWhu84a')
    message = await bot.send_message(call.message.chat.id, 'Ты выбрал спокойный маршрут, хороший выбор)\nТебе нужно обойти церковь через диспетч'
                                  'ерскую станцию, перейти дорогу, и подняться вверх в гору через деревню Сыркаши.\nП'
                                  'ервое что ты пройдешь будет пиццерия «Радора», затем небольшой поворот направо, затем н'
                                  'алево и прямо до конца, когда все дома будут позади тебя. На полянке ты увидишь справа тропинку,'
                                  ' по которой тебе и нужно подниматься. Наслаждайся природой и свежим воздухом во время подъема. Ка'
                                  'к только поднимешься, скажешь мне!')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/Gt9NfWrP/2024-08-01-163740496.png', reply_markup=exc1_calm)
    add_message_to_user_data(call.message.chat.id, message0.message_id)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_long')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message0 = await bot.send_message(call.message.chat.id, 'https://yandex.ru/maps/-/CDWhu84a')
    message = await bot.send_message(call.message.chat.id, 'Ты выбрал продолжительный маршрут, хороший выбор)\nСначала тебе нужно'
                                  ' добраться до Кузнецкого поворота, перейти дорогу и идти вдоль гаражей через деревню Сы'
                                  'ркаши, далее как дошли до Ул. Гастелло требуется пройти по диагонали вдоль 11 школы. После этого нужно и'
                                  'дти вперед до ближайшего поворота и повер'
                                  'нуть, далее идем вперед по протоптанной тропинке. Наслаждайся '
                                  'природой и свежим воздухом во время подъема. Как только поднимешься, скажешь мне!')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/9XNs9QtL/2024-08-01-163914817.png', reply_markup=exc1_long)
    add_message_to_user_data(call.message.chat.id, message0.message_id)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_sila')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message0 = await bot.send_message(call.message.chat.id, 'https://yandex.ru/maps/-/CDWhyC92')
    message = await bot.send_message(call.message.chat.id, 'Ты выбрал маршрут силы, хороший выбор)\nСначала тебе нужно добраться до Кузнецкого пово'
                                  'рота, перейти дорогу и идти вдоль гаражей через деревню Сыркаши, далее как дошли до Ул. Гаст'
                                  'елло и по диагонали пройти вдоль 11 школы. Потом тебе нужно идти вперед до ближайшего поворота и п'
                                  'овернуть, далее идем вперед п'
                                  'о протоптанной тропинке, затем поворот направо и вперед.Наслаждайся природой и свежи'
                                  'м воздухом во время подъема. Как только поднимешься, скажешь мне!')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/7YS8yy0X/2024-08-01-164029154.png', reply_markup=exc1_sila)
    add_message_to_user_data(call.message.chat.id, message0.message_id)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc1_final')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://imgur.com/a/09oK9Kn')
    message = await bot.send_message(call.message.chat.id, 'Поздравляю! Ты поднялся на вершину, можешь оглядеться и запечатлеть красивые виды нашего края! На этом мы подходим к концу, будем ждать тебя в будущем!', reply_markup=menu)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='sila_end')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Ты на месте. Камень силы был открыт в 2020 году Макеевым Федором Алексеев'
                                  'ичем. Волонтеры из совета ветеранов участвовали в раскопках. После раскопок и '
                                  'геологической экспертизы, оказалось, что камень'
                                  ' уходит в землю на 100 метров. \nВ народе считается камень имеет силу, которая помогает детям и беременным.')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/TP7Bc2v2/2024-08-01-164059500.png',
                                    reply_markup=menu)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Ответишь на мой вопрос и можем начинать!')
    message1 = await bot.send_message(call.message.chat.id, 'Как думаешь, сколько человек живет в Междуреченске?', reply_markup=exc2_ans1)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_false_ans1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '❌Подумай точнее!❌', reply_markup=exc2_again_ans1)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_true_ans1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, '✅Верно!✅ \n В Междуреченске проживает более 96.000 человек!')
    message1 = await bot.send_message(call.message.chat.id, 'А ведь это почти как в столице Шри-Ланки!')
    message2 = await bot.send_message(call.message.chat.id, 'Теперь можем начать нашу увлекательную экскурсию!')
    message3 = await bot.send_message(call.message.chat.id, 'Отправляю точку начала нашей эксурсии \n https://yandex.ru/maps/-/CCUOREsxsA')
    message4 = await bot.send_message(call.message.chat.id, 'Как будешь там, нажми на кнопку!', reply_markup=exc2_start)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_start')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Поздравляю ты на месте!')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/sxCnXYmG/2024-08-01-152241443.png')
    message2 = await bot.send_message(call.message.chat.id, 'Это каток на Брянской, он находится на открытом воздухе в глубинке микрорайона  «Западный». Здесь кажд'
                                   'ый год заливают каток. Катаясь на нем, вы отлично проведете время с друзьями или с семьей. Желательно '
                                   'идти кататься вечером, когда он освещается красивыми гирляндами.', reply_markup = exc2_ans2)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_ans2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Отлично, двигаемся дальше. Идем по маршруту вперед, между домов.')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/HLfzZwfv/2024-08-01-152327265.png')
    message2 = await bot.send_message(call.message.chat.id, 'Мы вышли на улицу Пушкина, продолжаем идти вперед.')
    message3 = await bot.send_message(call.message.chat.id, 'Немного пройдя по улице, мы увидим Городской дом культуры Железнодорожник.')
    message4 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/T1x9GR2r/2024-08-01-152354430.png')
    message5 = await bot.send_message(call.message.chat.id, 'На его площади мы наблюдаем праздничную ёлку и детский городок. Это место для от'
                                  'дыха детей и родителей Западного'
                                  ' района. Тут будет приятно провести время всем. Дети будут радов'
                                  'аться катанием с горки , а родители наслаждаться красотой вокруг себя.')
    message6 = await bot.send_message(call.message.chat.id, 'А в самом Доме культуры есть множество коллективов различных направлений. \n В ГДК «Железнод'
                                                            'орожник» работают творческие коллективы различных жанровых направлений. А зимой её украшают и ставят елку, горки.', reply_markup = exc2_point3)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_point3')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/hv00tHhN/2024-08-01-152426978.png')
    message2 = await bot.send_message(call.message.chat.id, 'Возвращаемся на аллею и идем вперед.')
    message3 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/htNVcSpf/2024-08-01-152449768.png')
    message4 = await bot.send_message(call.message.chat.id, 'Через некоторое время мы увидим красное двухэтажное здание, перед ним нужно повернуть налево.')
    message5 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/sDQXy584/2024-08-01-152511568.png')
    message6 = await bot.send_message(call.message.chat.id, 'Пройдя аллею, ориентируемся на магазин "яблоко Краснодар" и поворачиваем направо, держим путь вперед.')
    message7 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/sDrjFbYs/2024-08-01-152534312.png')
    message8 = await bot.send_message(call.message.chat.id,
                                      'И вот мы дошли до Праздничной площади.')
    message9 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/9XvvsTj9/2024-08-01-152757984.png')
    message10 = await bot.send_message(call.message.chat.id,
                                      'Площадь «Праздничная» в Междуреченске изначально была пустырём. Но каждый год здесь устанавливали елку '
                                  'и снежные городки.А 2020 году площадь благо'
                                  'устроили и теперь это неотъемлемая часть города. На ней вы точно не заскучаете. '
                                  'Елка, горки, зимние аттракционы - всё что нужно выходным зимним днем.', reply_markup = exc2_point4)

    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    add_message_to_user_data(call.message.chat.id, message7.message_id)
    add_message_to_user_data(call.message.chat.id, message8.message_id)
    add_message_to_user_data(call.message.chat.id, message9.message_id)
    add_message_to_user_data(call.message.chat.id, message10.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_point4')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Следуем вперед')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/Ghs12RCZ/2024-08-01-153037174.png')
    message2 = await bot.send_message(call.message.chat.id, 'Переходим дорогу и идем вдоль "ТЦ РАЙОН"')
    message3 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/brmHcW6g/2024-08-01-153123796.png')
    message4 = await bot.send_message(call.message.chat.id, 'Проходим тунель и поворачиваем налево')
    message5 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/gctZpVzg/2024-08-01-153143234.png')
    message6 = await bot.send_message(call.message.chat.id, 'И вот мы уже на центральной улице Междуреченска - проспект Коммунистический.', reply_markup = exc2_point5)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_point5')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Супер! Идем по проспекту до МГСТ и и наслаждаемся его культурой. Как увидим бежево-оранжевое здание, перед ним поворачиваем налево.')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/B6K7cSnF/2024-08-01-153540964.png')
    message2 = await bot.send_message(call.message.chat.id,
                                     'Идем до пешеходного перехода на кинотеатре “Кузбасс”. Если вы замерзли,можно зайти и попить чай в кафе на 2 этаже.' , reply_markup = exc2_point6)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_point6')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Справа от кинотеатра нас встречает Городской парк города Междуреченска, проходим немного вп'
                                  'еред и видим горку на которой можно с удовольствием покататься')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/DyMsFqg2/2024-08-01-153610098.png', reply_markup=exc2_point7)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_point7')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Идем дальше по парку, наблюдая зимнюю красоту природы')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/t46zMSj0/2024-08-01-153747169.png')
    message2 = await bot.send_message(call.message.chat.id, 'Далее нас встречает Монумент Славы Великой Отечественной Войны, как дойдем до него поворачиваем налево, в сторону дамбы')
    message3 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/tCQdVd62/2024-08-01-153806309.png', reply_markup = exc2_point8)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_point8')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Мы добрались до лыжероллерной трассы, зимой тут катаются на лыжах, что м'
                                  'ожете сделать и вы. Если вдруг у вас не оказалось с собой лы'
                                  'ж, не проблема! Рядом с домом спорта есть прокат')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/7LGbVd87/2024-08-01-153838355.png')
    message2 = await bot.send_message(call.message.chat.id, 'Время работы проката Дома спорта c 8:00 до 20:00 \n Цены: \n1 час - 129 р \nПоследующие - 100 р')
    message3 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/63Kwvm9B/2024-08-01-153900584.png', reply_markup = exc2_point9)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_point9')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Двигаемся в обратную сторону до Монумента Славы Великой Отечественной Войны,обходим его и идем вперед до пешеходного перехода')
    message1 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/W45Ldbfw/2024-08-01-154024406.png')
    message2 = await bot.send_message(call.message.chat.id, 'Переходим пешеходный переход и идем до Коммунистического проспекта')
    message3 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/0jMbt4Jh/2024-08-01-154147819.png')
    message4 = await bot.send_message(call.message.chat.id,
                                      'Мы дошли до второго катка под открытым небом, протяженностью 300 метров. Здес'
                                  'ь каждый вечер толпы счастливых людей катаются под ярко-сверкающей гирляндой. А'
                                  ' если вдруг у вас не оказалось коньков с собой, их можно взять в «Прокате №1'
                                  '» в доме ул. Весенней 12. Его режим работы с 10:00 до 20:00 без выходных')
    message5 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/3wx2TY4v/2024-08-01-154211043.png')
    message6 = await bot.send_message(call.message.chat.id, '1 час - 200 рублей\n2 часа - 250 рублей\n3 часа - 300 рублей\nДень - 400 рублей\nСутки - 500 рублей', reply_markup=exc2_point10)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_point10')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/DZjTMdVG/2024-08-01-154442916.png')
    message1 = await bot.send_message(call.message.chat.id, 'Сразу после катка нас встречает площадь весенняя. на которой стоит самая большая елка в городе'
                                  '. На ней: красивые фигуры из льда, ооогромная сверкающая елка, горки и множес'
                                  'тво другого. Идеальна для семейного зимнего вечера', reply_markup=exc2_end)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc2_end')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'И вот экскурсия подошла к концу')
    message1 = await bot.send_message(call.message.chat.id, 'Вы большой молодец! Проделали путь длиной 4,4 км.  Это стоило того :)', reply_markup=menu)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'Давай начнем экскурсию!')
    message1 = await bot.send_message(call.message.chat.id, 'Высылаю точку!\nhttps://yandex.ru/maps/-/CCUbzXRjkC')
    message2 = await bot.send_message(call.message.chat.id, 'А пока ты добираешься, я расскажу тебе небольшой факт о проспекте Коммунистическом!')
    message3 = await bot.send_message(call.message.chat.id, 'Проспект построен на том месте, где раньше протекала маленькая речка с заболоченными'
                                                            ' берегами. В прошлом столетии, а именно, в 50-х годах, улица носила название'
                                                            ' «6-й проезд». В 1957г улица получила другое название, более созвучное духу'
                                                            ' времени - проспект Коммунистический')
    message4 = await bot.send_photo(call.message.chat.id,
                                    photo='https://imgur.com/a/jQ3c4wQ')
    message5 = await bot.send_message(call.message.chat.id, 'Долгое время улица была предназначена для проезда автотранспорта.'
                                                            ' Границей между улицей и пешеходной зоной служила аллея, на '
                                                            'которой были высажены клены и тополя. Власти города решили '
                                                            'провести полную реконструкцию проспекта, и 23 июня 2003 г. '
                                                            'проспект предстал перед жителями в новом, современном, обличье.')
    message6 = await bot.send_message(call.message.chat.id, 'Как дойдешь, дай мне знать!', reply_markup=exc3_point1)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/Pf7BB57B/2024-08-01-155035737.png')
    message1 = await bot.send_message(call.message.chat.id, 'Перед тобой памятник В.И.Ленину, который был выполнен в 1961 году, и открывает проспект Коммунист'
                                  'ический')
    message2 = await bot.send_message(call.message.chat.id, 'Вождь Октябрьской революции 1917 г. представле'
                                  'н в полторы величины натурального роста, вс'
                                  'его же памятник вместе с постаментом составляет 7,9 метра')
    message3 = await bot.send_message(call.message.chat.id, 'В 2006 году состоялась реконструкция памятника - осн'
                                  'ование было укреплено, мраморная облицовка постам'
                                  'ента заменена гранитной, оформлена территория вокруг'
                                  ' памятника, сделана подсветка', reply_markup=exc3_point2)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/sgdbg0sm/2024-08-01-155104349.png')
    message1 = await bot.send_message(call.message.chat.id, 'Далее нас встречает мост через искусственный водоём')
    message2 = await bot.send_message(call.message.chat.id, 'На нём каждые молодожены могут повесить замок в знак вечной любви друг к другу', reply_markup=exc3_point3)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point3')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/Y0LypQPT/2024-08-01-155123876.png')
    message1 = await bot.send_message(call.message.chat.id, 'Перед тобой солнечные часы в честь 100 летия ленинского комсомола')
    message2 = await bot.send_message(call.message.chat.id, 'Тень от стального шипа падает на деления на тротуаре, по которым, с'
                                  'обственно, и можно узнать время!')
    message3 = await bot.send_message(call.message.chat.id, 'Как ты думаешь, какова высота шипа на часах?', reply_markup=exc3_query1)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_false1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '❌Подумай лучше!❌', reply_markup=exc3_query1)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_true1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '✅Молодец!✅')
    message2 = await bot.send_message(call.message.chat.id, 'Как только закончишь любоваться солнечными часами мы по'
                                  'йдем дальше по проспекту', reply_markup=exc3_point4)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point4')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/FRSN6kZs/2024-08-01-160736190.png')
    message1 = await bot.send_message(call.message.chat.id, 'Далее мы будем встречать на домах таблички, на которых указано какой известный человек жил в этом доме!')
    message2 = await bot.send_message(call.message.chat.id, 'Эта табличка расположена по адресу Коммунистический проспект 7, но чтобы тебе было легче их найти, я буду отправлять геометки')
    message3 = await bot.send_message(call.message.chat.id, 'https://yandex.ru/maps/-/CDGbv8kH', reply_markup=exc3_point5)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point5')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/6qLwWsgk/2024-08-01-160929579.png')
    message1 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/NG1Q7TFd/2024-08-01-160940176.png')
    message2 = await bot.send_message(call.message.chat.id, 'Обе табличку находятся на одном доме с разных сторон')
    message3 = await bot.send_message(call.message.chat.id, 'https://yandex.ru/maps/-/CDGb7Epj', reply_markup=exc3_point6)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point6')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/DZ136kvS/2024-08-01-161036753.png')
    message1 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/TPzXnY68/2024-08-01-161016943.png')
    message2 = await bot.send_message(call.message.chat.id, 'Дальше нас встречают две небольшие скульптуры мальчика и дев'
                                  'очки сидящих на шарах, а между ними находится световой фонтан!')
    message3 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/SRqFtTRD/2024-08-01-161053165.png')
    message4 = await bot.send_message(call.message.chat.id, 'Раньше из фонтана струями шла вода, но из-за дорогого обслуживания и травмоопасности его переделали под светящийся')
    message5 = await bot.send_message(call.message.chat.id,
                                      'Поэтому зимой 2019г в центре города уже красовался светодиодный фонтан Медуза!')
    message6 = await bot.send_message(call.message.chat.id,
                                      'Иди справа по проспекту, там ты увидешь очередную табличку!\nhttps://yandex.ru/maps/-/CDGfUMy4')
    message7 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/4NfR6Sr3/2024-08-01-161113652.png', reply_markup=exc3_point7)

    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    add_message_to_user_data(call.message.chat.id, message7.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point7')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/Z5gkhK09/2024-08-01-161135701.png')
    message2 = await bot.send_message(call.message.chat.id, 'Эти часы были установлены в 2004 году и они показывают время и .., и я забыл, можешь подсказать?', reply_markup=exc3_query2)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_false2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '❌Мне кажется другое❌', reply_markup=exc3_query2)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_true2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '✅Отлично!✅')
    message2 = await bot.send_message(call.message.chat.id, 'Дальше по проспекту тебя ждут еще инсталляции, пойдем посмотрим!')
    message3 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/YCvV8K8t/2024-08-01-161158255.png')
    message4 = await bot.send_message(call.message.chat.id, 'Как увидишь длинное здание, скажи мне!', reply_markup=exc3_point8)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point8')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/yNBmx0D2/2024-08-01-161219022.png')
    message2 = await bot.send_message(call.message.chat.id, 'Это - Государственное бюджетное профессиональное '
                                  'образовательное учреждение Междуреченский горностроительный техникум')
    message3 = await bot.send_message(call.message.chat.id, 'Или же по простому МГСТ')
    message4 = await bot.send_message(call.message.chat.id, 'В этом учебном заведении молодежь учится на такие профессии как: Слес'
                                  'арь; Электрослесарь по обслуживанию и ремонту обору'
                                  'дования. Горный техник-маркшейдер. Горный техник-те'
                                  'хнолог. Специалист по горным работам.')
    message5 = await bot.send_message(call.message.chat.id, 'Также мы увидим последнюю табличку на краю МГСТ')
    message6 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/KjKLwNW3/2024-08-01-161227725.png', reply_markup=exc3_point9)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point9')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/7Zr7tSnb/2024-08-01-161309940.png')
    message2 = await bot.send_message(call.message.chat.id, 'Мы подобрались к главной площади Комму'
                                  'нистического проспекта - к площади Согласия!')
    message3 = await bot.send_message(call.message.chat.id, 'Площадь представляет собой парковую зону, где вы'
                                  'сажено множество цветов и деревьев, установлены скамейки')
    message4 = await bot.send_message(call.message.chat.id, 'По праздникам здесь традиционно работают аниматоры для детей, а для'
                                  ' взрослых открывается танцевальная площадка!')
    message5 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/VNDCNpQb/2024-08-01-161319936.png')
    message6 = await bot.send_message(call.message.chat.id, 'Это не просто фонтан, а цветомузыкальный фонтан!')
    message7 = await bot.send_message(call.message.chat.id, 'Как думаешь когда он был построен?', reply_markup=exc3_query3)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    add_message_to_user_data(call.message.chat.id, message7.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_false3')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '❌Неверно❌', reply_markup=exc3_query3)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_true3')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '✅Да, ты прав!✅')
    message2 = await bot.send_message(call.message.chat.id, 'Цветомузыкальный фонтан на площади согласия был откр'
                                  'ыт 22 июня 2005 года к 50-летию Междуреченска')
    message3 = await bot.send_message(call.message.chat.id, 'Фонтан имеет диаметр 18 метров и высоту струи 9 метров\nПо мнению специалистов, в воздухе одновремен'
                                  'но находится около 200 литров воды')
    message4 = await bot.send_message(call.message.chat.id, 'Фонтан на Площади Согласия стал излюбленным местом встреч, отд'
                                  'ыха, поиска родственников и друзей!')
    message5 = await bot.send_message(call.message.chat.id, 'А до установки фонтана на площади были трибуны с'
                                  ' которых руководство города принимала парады')
    message6 = await bot.send_message(call.message.chat.id, 'Также это площадь знаменита тем, что в 1989 го'
                                  'ду здесь начались первые шахтерские забастовки', reply_markup=exc3_point10)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point10')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/23RqJfvg/2024-08-01-161354763.png')
    message2 = await bot.send_message(call.message.chat.id, 'Справа от фонтана располагается Отдел МВД России по городу Междуреченску')
    message3 = await bot.send_message(call.message.chat.id, 'Непростая это работа - охрана общественного порядка')
    message4 = await bot.send_message(call.message.chat.id, 'В Междуреченске началась она в период строительства первых предприя'
                                  'тий города, когда было всего несколько милиционеров из Мысковского '
                                  'отделения милиции')
    message5 = await bot.send_message(call.message.chat.id, 'Дежурили по два человека в Ольжерасе, Междуречье, Центральной части города')
    message6 = await bot.send_message(call.message.chat.id, 'Приказом МВД СССР от 18 сентября 1955 года был'
                                  'о объявлено о создании ОВД города Междуреченска\nЧисленность которого стала 74 человека', reply_markup=exc3_point11)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point11')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/9QBpGxHc/2024-08-01-161419504.png')
    message2 = await bot.send_message(call.message.chat.id, 'Слева располагается скульптура “По стопам отца” в честь областного Дня шахтера')
    message3 = await bot.send_message(call.message.chat.id, 'А ты знал что её открыли в…', reply_markup=exc3_query4)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_false4')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '❌Неверно❌', reply_markup=exc3_query4)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_true4')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, '✅Точно!✅')
    message1 = await bot.send_message(call.message.chat.id, 'Композиция “По стопам отца” изображает присевшего '
                                  'передохнуть шахтера и его маленького сына, который,'
                                  ' встретив отца с рабочей смены, решил примерить его к'
                                  'аску и рассказать, как прошел его день')
    message2 = await bot.send_message(call.message.chat.id, 'Следующей нашей контрольной точкой будет площадь Весенняя')
    message3 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/QtFJZh9M/2024-08-01-161439714.png', reply_markup=exc3_point12)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point12')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message0 = await bot.send_photo(call.message.chat.id,
                                    photo='https://i.postimg.cc/QtFJZh9M/2024-08-01-161439714.png')
    message = await bot.send_message(call.message.chat.id, 'Площадь Весенняя - это основное место п'
                                  'роведения общегородских мероприятий')
    message1 = await bot.send_message(call.message.chat.id, 'Здесь проводят праздники, ярмарки, торжествен'
                                  'ные линейки, выпускной, концерты, конкурсы и даже спортивные соревнования')
    message2 = await bot.send_message(call.message.chat.id, 'А также на новый год здесь ставится огромная ёлка, строятся ледяные горки'
                                  ', лабиринты и много других развлечений для детей', reply_markup=exc3_point13)
    add_message_to_user_data(call.message.chat.id, message0.message_id)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_point13')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/qRWXkSyx/2024-08-01-161556417.png')
    message1 = await bot.send_message(call.message.chat.id, 'Завершающей точкой нашего приключения станет ДК Распадский')
    message2 = await bot.send_message(call.message.chat.id, 'Немного о его истории:\n30 апреля 1981 года строителями трестов «Т'
                                  'омусашахтострой» и «Кузбассгражданстрой» №1 был сдан в эксп'
                                  'луатацию Дворец Культуры шахты «Рас'
                                  'падская», алую ленточку порезал Первый секретарь горкома па'
                                  'ртии В.И Овдиенко')
    message3 = await bot.send_message(call.message.chat.id, 'Примечателен тот факт, что фундамент здания был '
                                  'заложен десятью годами ранее')
    message4 = await bot.send_message(call.message.chat.id, 'Подобно многим другим социальным объектам,'
                                  ' Дворец строился как ведомственное учреждение, на ср'
                                  'едства шахты «Распадской»')
    message5 = await bot.send_message(call.message.chat.id, 'Также дворец отреставрировали в…', reply_markup=exc3_query5)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_false5')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '❌Неверно❌', reply_markup=exc3_query5)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc3_true5')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '✅Ты гуру!✅')
    message2 = await bot.send_photo(call.message.chat.id,
                                       photo='https://i.postimg.cc/sxSP1mJd/2024-08-01-161622651.png')
    message3 = await bot.send_message(call.message.chat.id, 'Справа от здания Дк Распадского ты можешь увидеть открытую выставку картин, обязательно их посмотри!')
    message4 = await bot.send_message(call.message.chat.id, 'На этом мы подходим к концу, будем ждать тебя в будущем!\nЕсли хочешь иметь '
                                                            'доступ к искусственному интеллекту, а также дополнительные экскурсии, оформи платную подписку', reply_markup=menu)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    await call.answer()

@dp.callback_query_handler(text='gold_menu')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    sent_message = await bot.send_photo(call.message.chat.id,
        photo='https://i.postimg.cc/kgCdZ8d4/2024-08-01-151919786.png', reply_markup=gold)
    sent_message1 = await bot.send_message(call.message.chat.id,'Привет, я сурок Стёпа, и сегодня я проведу тебе одну из экскурсий!')
    sent_message2 = await bot.send_message(call.message.chat.id,'Ответишь на пару вопросов, чтобы я смог выбрать для тебя маршрут'
                         ' или хочешь сам?', reply_markup=gold_start)

    add_message_to_user_data(call.message.chat.id, sent_message.message_id)
    add_message_to_user_data(call.message.chat.id, sent_message1.message_id)
    add_message_to_user_data(call.message.chat.id, sent_message2.message_id)
    await call.answer()

@dp.callback_query_handler(lambda c: c.data == 'gold_sam')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, 'У нас есть 6 экскурсии, 2 в разных районах, 1 по всему городу, 1 за городом и 2 на гору!', reply_markup=gold_exc_var)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(lambda c: c.data == 'gold_ne_sam')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, "Ты бы хотел узнать историю улиц и достопримечательностей или пройтись по всему городу, а также взобраться на гору?", reply_markup=gold_start_var)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='gols_start_var1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, "К чему ты ближе, к вокзалу или к памятнику Ленина?", reply_markup=gold_start_var1)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='gold_start_var2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, "Ты хочешь посмотреть на сфинксов и отдохнуть или пройти весь город и взобраться на гору?", reply_markup=gold_start_var1)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc5')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, "Давай начнем экскурсию!")
    message1 = await bot.send_message(call.message.chat.id, "Высылаю точку, к которой тебе нужно будет добраться\nhttps://yandex.ru/maps/-/CDWMiWYs")
    message2 = await bot.send_photo(call.message.chat.id,
        photo='AgACAgIAAxkBAAIF7Waf2adwQtmAjbHXchLhnW77ko1yAAJ56TEb840BSU7lFZMWkY2PAQADAgADeAADNQQ')
    message3 = await bot.send_message(call.message.chat.id, "Санаторий находится за городом, поэтому до него проще доехать на автобусе или на машине.\nДо него идут следующие автобусы: 11, 11/б, 12", reply_markup=exc5)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc5_point1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message = await bot.send_message(call.message.chat.id, "Это санаторно-оздоровительный центр, в котором вы можете хорошо провести время")
    message1 = await bot.send_message(call.message.chat.id, "Санаторий предоставляет путевки на неделю и на месяц, а также посуточно. Отдельно вы можете арендовать сауну, беседку с bbq, обеденный зал и другое")
    message2 = await bot.send_message(call.message.chat.id, "Как думаешь, когда открылся санаторий?", reply_markup=exc5_query1)
    add_message_to_user_data(call.message.chat.id, message.message_id)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc5_false1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '❌Попробуй ещё раз❌', reply_markup=exc5_query1)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc5_true1')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, '✅Верно✅')
    message2 = await bot.send_message(call.message.chat.id, 'Именно тогда был открыт санаторий, а также у его входа скульптор поставил стража - Сфинкса. Он охраняет покой всех отдыхающих')
    message3 = await bot.send_photo(call.message.chat.id,
        photo='AgACAgIAAxkBAAIF72akk_by7e8eNfYwI9vy5T-a0D54AAI95jEbBDIgSYqpwsP-mpUuAQADAgADeQADNQQ')
    message4 = await bot.send_message(call.message.chat.id, 'Фигура представляет собой сфинкса с головой красноармейца и телом льва')
    message5 = await bot.send_message(call.message.chat.id, 'Первоначально вход на Романтику находился значительно правее современного входа.'
                                                            ' Правый повород после переезда на дорогу ведёт нас к старому входу в санаторий')
    message6 = await bot.send_photo(call.message.chat.id,
        photo='AgACAgIAAxkBAAIF8WalLiUxxh1wOJzqQmZTYbANa-W-AALJ3DEba9coSXnTLcup7myXAQADAgADeAADNQQ')
    message7 = await bot.send_message(call.message.chat.id, 'А вот и сфинкс!\nВремя, ветер, дождь и снег сделали свое дело и теперь сложно понять это голова красноармейца или льва', reply_markup=exc5_point2)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    add_message_to_user_data(call.message.chat.id, message2.message_id)
    add_message_to_user_data(call.message.chat.id, message3.message_id)
    add_message_to_user_data(call.message.chat.id, message4.message_id)
    add_message_to_user_data(call.message.chat.id, message5.message_id)
    add_message_to_user_data(call.message.chat.id, message6.message_id)
    add_message_to_user_data(call.message.chat.id, message7.message_id)
    await call.answer()

@dp.callback_query_handler(text='exc5_point2')
async def handle_callback(call: types.CallbackQuery):
    if call.message.chat.id in user_data:
        for message_id in user_data[call.message.chat.id]:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        user_data[call.message.chat.id] = []
    message1 = await bot.send_message(call.message.chat.id, 'Теперь ты можешь вернуться к основному входу и '
                                                            'пройти в свой номер, если ты его забронировал, а как отдохнешь обязательно дойди до искусственного озера!')
    message2 = await bot.send_photo(call.message.chat.id,
        photo='AgACAgIAAxkBAAIF82alM46iCSociehUg3wHxAH09616AALe3DEba9coSfIUEfLRLT2EAQADAgADeQADNQQ')
    message3 = await bot.send_message(call.message.chat.id, 'Раньше на его месте был лог, но после рещили создать озеро, глубиной в 7 метров!')
    message3 = await bot.send_message(call.message.chat.id, 'На этом наша экскурсия подходит к концу! Если захочешь пройти ещё - выбери в меню', reply_markup=gold_menu)
    add_message_to_user_data(call.message.chat.id, message1.message_id)
    await call.answer()

@dp.message_handler(content_types=ContentType.PHOTO)
async def send(message: Message):
    await message.reply(message.photo[-1].file_id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_polling(dp, skip_updates=True)