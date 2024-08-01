from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, types
menu = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Меню', callback_data='menu'))
start_var = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Cпортзал', callback_data='gora'),
                                            (InlineKeyboardButton(text='Музей', callback_data='exc3')))
queue = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Летом', callback_data='exc3'),
                                            (InlineKeyboardButton(text='Зимой', callback_data='exc2')))
longorshort = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='По городу', callback_data='exc3'),
                                            (InlineKeyboardButton(text='На гору', callback_data='big_in_priroda')))
start = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Подбери маршрут', callback_data='ne_sam'),
                                          (InlineKeyboardButton(text='Выберу сам', callback_data='sam')))
exc1_point0 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Я на месте', callback_data='mesto-1'))
exc1_point1 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Я на смотровой площадке!', callback_data='exc1_point-1'))
exc1_ans1 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='216 км', callback_data='exc1_false_ans1'),
                                              (InlineKeyboardButton(text='3255 км', callback_data='exc1_false_ans1')),
                                               (InlineKeyboardButton(text='179 км', callback_data='exc1_true_ans1')))
exc1_again_ans1 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Попробовать ещё раз', callback_data='exc1_point-1'))
exc1_point2 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Вижу Лысую гору', callback_data='exc1_point-2'))
exc1_point3 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Идём дальше', callback_data='exc1_point-3'))
exc1_ans2 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='В 1952 году', callback_data='exc1_true_ans2'),
                                              (InlineKeyboardButton(text='В 1967 году', callback_data='exc1_false_ans2')),
                                               (InlineKeyboardButton(text='В 1944 году', callback_data='exc1_false_ans2')))
exc1_again_ans2 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Попробовать ещё раз', callback_data='exc1_point-3'))
exc1_point4 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Я на месте!', callback_data='exc1_point4'))
exc1_point5 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Пошли дальше!', callback_data='exc1_point5'))
exc1_point6 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='У репки!', callback_data='exc1_point6'))
exc1_ans3 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='"Маша и Медведь"', callback_data='exc1_false_ans3'),
                                              (InlineKeyboardButton(text='"Вершки и корешки"', callback_data='exc1_true_ans3')),
                                               (InlineKeyboardButton(text='"Репка"', callback_data='exc1_false_ans3')))
exc1_again_ans3 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Попробовать ещё раз', callback_data='exc1_point6'))
exc1_point7 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Я у выхода!', callback_data='exc1_point7'))
exc1_ans4 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='"Русалочка"', callback_data='exc1_false_ans4'),
                                              (InlineKeyboardButton(text='"Три богатыря"', callback_data='exc1_false_ans4')),
                                               (InlineKeyboardButton(text='"Руслан и Людмила"', callback_data='exc1_true_ans4')))
exc1_again_ans4 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Попробовать ещё раз', callback_data='exc1_point7'))
exc1_point8 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='У кинотеатра!', callback_data='exc1_point8'))
exc1_ans5 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='В 1956 году', callback_data='exc1_true_ans5'),
                                              (InlineKeyboardButton(text='В 1935 году', callback_data='exc1_false_ans5')),
                                               (InlineKeyboardButton(text='В 1966 году', callback_data='exc1_false_ans5')))
exc1_again_ans5 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Попробовать ещё раз', callback_data='exc1_point8'))
exc1_point9 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Вижу Гулливера!', callback_data='exc1_point9'))
exc1_point10 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='У Монумента Славы!', callback_data='exc1_point10'))
exc1_point11 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='На месте!', callback_data='exc1_point11'))
exc1_point12 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Вижу дома!', callback_data='exc1_point12'))
exc1_point14 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Подъем рядом с церковью', callback_data='exc1_up1'),
                                              (InlineKeyboardButton(text='Подъем через 11 школу', callback_data='exc1_up2')))
exc1_ans6 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='В Сосновке', callback_data='exc1_false_ans6'),
                                              (InlineKeyboardButton(text='В Таёжке', callback_data='exc1_false_ans6')),
                                               (InlineKeyboardButton(text='В Старом Междуречье', callback_data='exc1_true_ans6')))
exc1_again_ans6 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Попробовать ещё раз', callback_data='exc1_point12'))
exc1_point13 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='На месте!', callback_data='exc1_point13'))
exc1_point15 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Я на развилке!', callback_data='exc1_point15'))
exc1_end = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Закончить экскурсию', callback_data='exc1_end'))
exc1_gora = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='В меню', callback_data='exc1_menu'),
                                                  (InlineKeyboardButton(text='Сыркашинская', callback_data='gora')))
puti = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Экстремальный', callback_data='exc1_extreme'),
                                              (InlineKeyboardButton(text='Спокойный', callback_data='exc1_calm')),
                                               (InlineKeyboardButton(text='Продолжительный', callback_data='exc1_long')),
                                             (InlineKeyboardButton(text='Маршрут силы', callback_data='exc1_sila')))
exc1_extreme = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Я на месте', callback_data='exc1_final'))
exc1_long = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Я на месте', callback_data='exc1_final'))
exc1_calm = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Я на месте', callback_data='exc1_final'))
exc1_sila = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Я на месте', callback_data='sila_end'))
exc1_menu = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='В меню', callback_data='exc1_menu'))
dis = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Я в западном!', callback_data='exc2'),
                                              (InlineKeyboardButton(text='Я в восточном!', callback_data='exc3')))
exc2_ans1 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='80.000', callback_data='exc2_false-ans1'),
                                              (InlineKeyboardButton(text='107.385', callback_data='exc2_false_ans1')),
                                               (InlineKeyboardButton(text='96.000', callback_data='exc2_true_ans1')))
exc2_again_ans1 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Попробовать ещё раз', callback_data='exc2'))
exc2_start = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Я на месте!', callback_data='exc2_start'))
exc2_ans2 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Я на месте!', callback_data='exc2_ans2'))
exc2_point3 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идем дальше!', callback_data='exc2_point3'))
exc2_point4 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Двигаемся дальше!', callback_data='exc2_point4'))
exc2_point5 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Держим путь вперед!', callback_data='exc2_point5'))
exc2_point6 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Я на месте!', callback_data='exc2_point6'))
exc2_point7 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Накатался!', callback_data='exc2_point7'))
exc2_point8 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Я на дамбе!', callback_data='exc2_point8'))
exc2_point9 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Дальше', callback_data='exc2_point9'))
exc2_point10 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Отправляемся!', callback_data='exc2_point10'))
exc2_end = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Всё!', callback_data='exc2_end'))
exc3_point1 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point1'))
exc3_point2 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point2'))
exc3_point3 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point3'))
exc3_point4 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point4'))
exc3_point5 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point5'))
exc3_point6 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point6'))
exc3_point7 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Вижу часы', callback_data='exc3_point7'))
exc3_point8 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point8'))
exc3_point9 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point9'))
exc3_point10 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point10'))
exc3_point11 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point11'))
exc3_point12 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point12'))
exc3_point13 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Идём дальше!', callback_data='exc3_point13'))
exc3_query1 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='5м', callback_data='exc3_false1'),
                                              (InlineKeyboardButton(text='6м', callback_data='exc3_true1')),
                                               (InlineKeyboardButton(text='7м', callback_data='exc3_false1')))
exc3_query2 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Температуру и дату', callback_data='exc3_true2'),
                                              (InlineKeyboardButton(text='Скорость ветра и дату', callback_data='exc3_false2')),
                                               (InlineKeyboardButton(text='Атмосферное давление и температуру', callback_data='exc3_false2')))
exc3_query3 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='В 2005', callback_data='exc3_true3'),
                                              (InlineKeyboardButton(text='В 2004', callback_data='exc3_false3')),
                                               (InlineKeyboardButton(text='В 2006', callback_data='exc3_false3')))
exc3_query4 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='2019г', callback_data='exc3_false4'),
                                              (InlineKeyboardButton(text='2016г', callback_data='exc3_false4')),
                                               (InlineKeyboardButton(text='2017г', callback_data='exc3_true4')))
exc3_query5 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='в 2000г', callback_data='exc3_false5'),
                                              (InlineKeyboardButton(text='в 2005г', callback_data='exc3_true5')),
                                               (InlineKeyboardButton(text='в 2010г', callback_data='exc3_false5')))
exc_var = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Зимние Забавы', callback_data='exc2'),
                                              (InlineKeyboardButton(text='Прогулка по Коммунистическому проспекту', callback_data='exc3')),
                                               (InlineKeyboardButton(text='Городская', callback_data='big_in_priroda')),
                                                (InlineKeyboardButton(text='гора Сыркашинская', callback_data='gora')))
podpiska = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Приобрести подписку', callback_data='subscribe'),
                                          (InlineKeyboardButton(text='Отменить подписку', callback_data='unsubscribe')))
gold_menu = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Меню', callback_data='gold_menu'))
gold_start = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Подбери маршрут', callback_data='gold_ne_sam'),
                                          (InlineKeyboardButton(text='Выберу сам', callback_data='gold_sam')))
gold_exc_var = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Зимние Забавы', callback_data='exc2'),
                                              (InlineKeyboardButton(text='Прогулка по Коммунистическому проспекту', callback_data='exc3')),
                                               (InlineKeyboardButton(text='Городская', callback_data='big_in_priroda')),
                                                (InlineKeyboardButton(text='гора Сыркашинская', callback_data='gora')),
                                                (InlineKeyboardButton(text='гора Югус', callback_data='gora_ugus')),
                                                (InlineKeyboardButton(text='Путешествия к Cфинксу', callback_data='sfinks')),
                                                (InlineKeyboardButton(text='Прогулка до мемориала', callback_data='sfinks')))
gold_start_var = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Горы', callback_data='gold_start_var2'),
                                            (InlineKeyboardButton(text='История улиц', callback_data='gols_start_var1')))
gold_start_var1 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='К Ленину', callback_data='exc3'),
                                            (InlineKeyboardButton(text='К вокзалу', callback_data='big_in_priroda')))
gold_start_var2 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='гора Сыркашинская', callback_data='exc5'),
                                            (InlineKeyboardButton(text='Весь город', callback_data='big_in_priroda')),
                                            (InlineKeyboardButton(text='Поездка к Сфиксам', callback_data='gora')))
exc5 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Приехал!', callback_data='exc5_point1'))
exc5_query1 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='В 1959', callback_data='exc5_false1'),
                                              (InlineKeyboardButton(text='В 1966', callback_data='exc5_true1')),
                                               (InlineKeyboardButton(text='В 1963', callback_data='exc5_false1')))
exc5_point2 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Дальше!', callback_data='exc5_point2'))
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button = types.KeyboardButton('Вернуться в меню')
subscribe_butt = types.KeyboardButton('Платная подписка')
keyboard.add(button, subscribe_butt)

gold = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
button_gold = types.KeyboardButton('Платное меню')
subscribe_butt = types.KeyboardButton('Платная подписка')
gold.add(button_gold, subscribe_butt)