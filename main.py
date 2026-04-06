from importt import *

from db_manage import *
@dp.message_handler(commands=['start'])
async def start_com(message: types.Message):
    await inicialization(message.chat.id)  # ДОБАВЛЯЕЮ ЮЗЕРА А БД

    if message.chat.id == ID_ADMIN:
        one = InlineKeyboardButton('Заснуть легко', callback_data='audio:one')
        two = InlineKeyboardButton('Границы чувств', callback_data='audio:two')
        three = InlineKeyboardButton('Таблетка от стресса', callback_data='audio:three')
        four = InlineKeyboardButton('Таблетка от панической атаки', callback_data='audio:four')
        five = InlineKeyboardButton('Аудиотаблетка от ложного голода', callback_data='audio:five')
        link_on_chanel = InlineKeyboardButton('Наш канал', url='https://t.me/audioaptechka')
        stat = InlineKeyboardButton('Статистика', callback_data='static')
        rasssilka = InlineKeyboardButton('Рассылка', callback_data='rassilka')
        keyboard = InlineKeyboardMarkup(row_width=1).add(one, two, three, four, five, link_on_chanel).row(stat, rasssilka)
    else:
        one = InlineKeyboardButton('Заснуть легко', callback_data='audio:one')
        two = InlineKeyboardButton('Границы чувств', callback_data='audio:two')
        three = InlineKeyboardButton('Таблетка от стресса', callback_data='audio:three')
        four = InlineKeyboardButton('Таблетка от панической атаки', callback_data='audio:four')
        five = InlineKeyboardButton('Аудиотаблетка от ложного голода', callback_data='audio:five')
        link_on_chanel = InlineKeyboardButton('Наш канал', url='https://t.me/audioaptechka')
        keyboard = InlineKeyboardMarkup(row_width=1).add(one, two, three, four, five, link_on_chanel)
    await bot.send_message(
        chat_id=message.chat.id,
        text='Выберите аудиотаблетку:',
        reply_markup=keyboard,
        parse_mode="MarkdownV2")

#ОТПРВКА АУДИО ФАЛЙЛА ИЛИ ПРОСЬБО ОПЛАТИТЬ
@dp.callback_query_handler(lambda c: c.data.startswith('audio'))
async def process_callback_params_any(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await process_callback_params_any_2(callback_query)

# СТАТИСТИКА
@dp.callback_query_handler(lambda c: c.data.startswith('static'))
async def static_function(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    count_users = await db_select_id_sys('chat_id')
    all_1 = []
    all_2 = []
    all_users = await db_select_id_sys('*') # ВСЯ ИНФА ПРО ПОЛЬЗОВАТЕЛЯ

    for i in range(len(all_users)):
        all_1.append(all_users[i][1])
        all_2.append(all_users[i][2])

    all_1 = all_1.count('True')
    all_2 = all_2.count('True')
    sum = ((all_1*5000) + (all_2*1000))
    await bot.send_message(chat_id=callback_query.from_user.id, text=f'Участников в боте: {len(all_users)}\nПродано на {sum} рублей')

# ЛОВИМ НАЖАТИЕ КНОПКИ РАССЫЛКА
@dp.callback_query_handler(lambda c: c.data.startswith('rassilka'))
async def rasilca_function(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # sub = await db_select_id_sys('chat_id')
    await update_rasslika('True')
    back = InlineKeyboardButton('Остановить рассылку', callback_data='back')
    keyb = InlineKeyboardMarkup(row_width=1).add(back)
    await bot.send_message(chat_id=ID_ADMIN, text = 'Отправьте сообщение в чат и оно прийдет всем пользователям бота. Поддерживаемые форматы: все', reply_markup=keyb)

# ОСУЩЕСТВЛЕНИЕ РАССЫЛКИ
@dp.message_handler()
async def ras(message: types.Message):
    a = await get_rasslika()
    x = 0
    if a[0][0] == 'True':
        sub = await db_select_id_sys('chat_id')
        for i in range(len(sub)):
            try:
                await bot.send_message(chat_id=sub[i][0], text=message.text)
                x += 1
            except:
                pass
    await bot.send_message(chat_id=ID_ADMIN, text = f'Рассылка прошла успешно!\nОтправлено {x} сообщений')
    await update_rasslika('False')

# ОТЛАВЛИВАНИЕ НАЖАНИЯ КНОПКИ НАЗАД ПРИ ВЫБОРЕ РАССЫЛКИ
@dp.callback_query_handler(lambda c: c.data.startswith('back'))
async def process_callback_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await update_rasslika('False')
    await bot.send_message(chat_id=callback_query.from_user.id, text='Рассылка отменена')


# ОЛАТА ИЛИ ОТПРАВКА ЗАПИСИ
async def process_callback_params_any_2(callback_query):
    audio = callback_query.data.split(':')
    if audio[1] in ['one', 'two']:
        a = await db_select_sys(audio[1], callback_query.message.chat.id)
        if a[0] == 'True':  # ЕСЛИ УЖЕ ОПЛАЧЕНО, ТО ВЫСЫЛАЕТСЯ АУДИО
            await bot.send_audio(chat_id=callback_query.message.chat.id, audio = arr_audio[audio[1]], caption=audio_txt[audio[1]],  protect_content=True)
        else:  # ОТПРАВКА ССЫЛКИ НА ОПЛАТУ
            pay_link = InlineKeyboardButton('Оплатить', url=await pay_method(callback_query.message.chat.id, prices[audio[1]], audio[1]))
            keyboard_button = InlineKeyboardMarkup(row_width=1).add(pay_link)
            await bot.send_message(callback_query.message.chat.id,
                                   text="Чтобы получить доступ к аудиозаписи, с начала нужно оплатить",
                                   reply_markup=keyboard_button,
                                   protect_content=True)
            # await asyncio.sleep(2)

            pay_link = InlineKeyboardButton('Я оплатил (а)', callback_data=f'check_pay_status:{audio[1]}')
            keyboard_button_2 = InlineKeyboardMarkup(row_width=1).add(pay_link)
            await bot.send_message(callback_query.message.chat.id,
                                   text="После оплаты нажмите кнопку, чтобы проверить статус оплаты. ",
                                   reply_markup=keyboard_button_2, protect_content=True)
    else:
        await bot.send_audio(chat_id=callback_query.message.chat.id, audio=arr_audio[audio[1]],  caption=audio_txt[audio[1]], protect_content=True) #caption=f'Аудио записть : {audio[1]}',

#################################################################################################################################
###########################################                  ОПЛАТА                   ###########################################
#################################################################################################################################


# ГЕНЕРАЦИЯ ССЫЛКИ ДЛЯ ОПЛАТЫ
async def pay_method(chat_id, num, audio_num):
    chek_pay_str = f"{audio_num}:{chat_id}:{await generate_random_string()}"
    await db_update_sys(f"{audio_num}_link", chat_id, chek_pay_str)
    link_on_pay = Quickpay(receiver=YOOMONEY_RECEIVER,
                        quickpay_form="shop",
                        targets="Sponsor this project",
                        paymentType="rub",
                        sum=num,
                        label=chek_pay_str)
    return link_on_pay.redirected_url



# ГЕНЕРАЦИЯ РАНДОМНОЙ СТРОКИ ДЛЯ УНАКАЛЬНОСТИ КАЖДОГО ПЛАТЕЖА
async def generate_random_string():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(15))
    return random_string

# ПРОВЕРКА ОПЛАТЫ
async def check_pay(chat_id, callback_query, num):
    comment = await db_select_sys(f"{num}_link", chat_id)
    try:
        history = client.operation_history(label=str(comment[0]))
        if history.operations == []:
            await bot.send_message(chat_id=chat_id, text="Сожалеем, но платеж не был обнаружен, попробуйте еще раз проверить нажав кнопку снова")
        else:
            for operation in history.operations:
                if operation.status == 'success':
                    await db_update_sys(num, chat_id, 'True')
                    await bot.send_message(chat_id=ID_ADMIN, text=f'Оплатили: {prices[num]}')
                    await process_callback_params_any_2(callback_query)

    except Exception as e:
        print(e)

#   ЛОВИМ НАЖАТИЕ КНОПКИ ДЛЯ ПРОВЕРКИ ПЛАТЕЖА
@dp.callback_query_handler(lambda c: c.data.startswith('check_pay_status'))
async def process_callback_params_any(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    ch_pay = callback_query.data.split(':')
    await check_pay(callback_query.from_user.id, callback_query, ch_pay[1])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
