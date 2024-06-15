from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb


router = Router()


class SupportState(StatesGroup):
    waiting_for_question = State()
    waiting_for_return = State()
    waiting_for_idea = State()
    waiting_for_job = State()
    waiting_for_answer = State()


@router.message(CommandStart())
async def echo(message: Message):
    await message.answer(f'<b>Йо, {message.from_user.first_name}, DANCE на связи 🥳</b>\n\nТут ты можешь найти ответы на все интересующие тебя вопросы!\nВыбери то, что ты бы хотел узнать, я тебе помогу, а если не смогу, то позову помощника\n\n<b><i>-Билеты 🏖️\n-Тех.поддержка 📞\n-Сотрудничество 👨‍💻\n-О нас 📚</i></b>', parse_mode='HTML', reply_markup=kb.main)


@router.callback_query(F.data == 'home')
async def echo(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f'<b>Йо, {callback.from_user.first_name}, DANCE на связи 🥳</b>\n\nТут ты можешь найти ответы на все интересующие тебя вопросы!\nВыбери то, что ты бы хотел узнать, я тебе помогу, а если не смогу, то позову помощника\n\n<b><i>-Билеты 🏖️\n-Тех.поддержка 📞\n-Сотрудничество 👨‍💻\n-О нас 📚</i></b>', parse_mode='HTML', reply_markup=kb.main)


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(f'<b>Добро пожаловать в раздел помощи, тут ты поймешь как пользоваться ботом!</b>\n\nПользуясь нашим ботом ты можешь узнать:<i>\n-Как покупать билеты?\n-Как с нами работать?\n-Кто мы такие?</i>\n\nДля этого просто выбирай то, что тебе интересно и узнаешь все!', parse_mode='HTML', reply_markup=kb.menu)


@router.callback_query(F.data == 'tickets')
async def get_tickets(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'<b>Ты попал на вкладку билеты</b>\nЗдесь ты можешь узнать всю интересующую тебя информацию о билетах\nВыбери то, что будет полезно для тебя:\n\n<b><i>\n-Где купить билет?\n-Как им пользоваться?</i></b>', parse_mode='HTML', reply_markup=kb.tickets)


@router.callback_query(F.data == 'wherePay')
async def where_pay(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'<b><i>На данный момент мы пользуемся сервисом <a href="https://orenburg.qtickets.events/106984-xxxmanera-21-aprelya">Qtickets</a></i></b>\n<i>Там ты и можешь купить билет на наши мероприятия</i>\n\n<b><i>Всю дополнительную информацию о мероприятиях ты можешь узнать в нашем телеграмм-канале @dvnce_events</i></b>', parse_mode='HTML', reply_markup=kb.ticketsBack)


@router.callback_query(F.data == 'howUse')
async def where_info_ticket(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'<b><i>Билет нужно показать нашему работнику на входе</i></b>\n\n<i>Если у вас остануться еще какие-то вопросы - спросите работников</i>\n\n<b><i>Где проходят мероприятия узнавать в нашем телеграмм-канале @dvnce_events</i></b>', parse_mode='HTML', reply_markup=kb.ticketsBack)


@router.callback_query(F.data == 'return')
async def get_return(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(f'Чтобы вернуть билет нужно:<b><i>\n-Отправить файл билета\n-Свою почту\n-Причина по которой вы не можете попасть на мероприятие\n\nПосле всех этих действий мы вернем вам деньги!\n\nОтправляйте все это одним сообщением, чтобы не нагружать специалистов!</i></b>\n\n<i>Возврат за 10 дней и более - 100% от стоимости билета\nВозврат от 9 до 5 дней - 50%\nВозврат от 4 до 3 дней - 30%\nМенеее трех дней - не принимаются к возврату</i>', parse_mode='HTML', reply_markup=kb.returnProccess)
    await state.set_state(SupportState.waiting_for_return)


@router.message(SupportState.waiting_for_return)
async def process_return_ticket(message: types.Message, state: FSMContext):
    return_text = message.text or message.caption
    return_document = None
    return_photo = None

    if message.document:
        return_document = message.document.file_id

    if message.photo:
        return_photo = message.photo[-1].file_id  # Выбираем последнюю фотографию из списка

    await state.update_data(returnTicket=return_text, returnDocument=return_document, returnPhoto=return_photo)

    await get_return_process_with_state(message, state)


async def get_return_process_with_state(message: types.Message, state: FSMContext):
    return_data = await state.get_data()
    return_text = return_data.get('returnTicket')
    return_document = return_data.get('returnDocument')
    return_photo = return_data.get('returnPhoto')

    user = message.from_user.username
    profile_link = f'@{user}'
    group_chat_id = '-4132933387'

    message_caption = f"<b><i>Пользователь {profile_link} хочет вернуть билет</i></b>"
    if return_text:
        message_caption += f"\n\nВот его данные:\n\n<blockquote>{return_text}</blockquote>\n\n"
    if return_document:
        await message.bot.send_document(group_chat_id, return_document, caption=message_caption, parse_mode='HTML')
    elif return_photo:
        await message.bot.send_photo(group_chat_id, return_photo, caption=message_caption, parse_mode='HTML')
    elif not return_text and not return_photo and not return_document:
        await message.answer(f"<b><i>Кажется, произошла ошибка.</i></b>\n\nПожалуйста, введите ваш запрос исключительно текстом, фоткой или файлом", parse_mode='HTML')
    else:
        await message.bot.send_message(group_chat_id, message_caption, parse_mode='HTML')

    await message.answer(f'Ваша заявка отправлена администраторам!\n\n<b><i>В скором времени денежные средства вернутся на ваш счет!</i></b>\n\n<b><i>Если у вас остались вопросы - обращайтесь в поддержку</i></b>', parse_mode='HTML', reply_markup=kb.menu)
    await state.clear()


@router.callback_query(F.data == 'infoTickets')
async def get_info(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'<i><b>• Танцпол</b> - Обычный билет, без каких-либо преимуществ с доступом только на танцпол\n\n• <b>Парный танцпол</b> - Билет рассчитанный на двоих людей, выгоднее покупать, чем <b>"Танцпол"</b>\n\n<b>• FAN-билет</b> - Билет, который даёт вам афишу с автографом артистов и ранний вход, чтобы вы могли занять самые лучшие места около сцены!\n\n<b>• Meet & Greet</b> - Билет, который даёт уникальную возможность встретиться с артистами вживую, а также фотосессия с хедлайнерами тусовки</i>\n\n<b><i>Все категории билетов действуют как входной билет, вам нужно покупать в дополнение билет категории <b>"Танцпол"</b>, если вы купили категорию выше <b>"Танцпол"</b></i></b>', parse_mode='HTML', reply_markup=kb.ticketsBack)


@router.callback_query(F.data == 'support')
async def get_support(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'<b>Ты попал на вкладку тех. поддержки</b>\nТут можешь задать любой вопрос и мы на него ответим как можно скорее!\n\n<b><i>Часы работы тех.поддержки: 10:00-00:00</i></b>', parse_mode='HTML', reply_markup=kb.techSupport)


@router.callback_query(F.data == 'tech')
async def get_tech(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(f'Опишите вашу проблему максимально подробно, чтобы наши сотрудники без труда могли вам помочь.\n\n<b>Далее просто нажми на "Отправить вопрос"!</b>\n\n<b><i>Максимальное время ответа в рабочие часы 10 минут!</i></b>', parse_mode='HTML', reply_markup=kb.askSupportment)
    await state.set_state(SupportState.waiting_for_question)


@router.message(SupportState.waiting_for_question)
async def process_tech_question_and_send(callback: CallbackQuery, state: FSMContext):
    question_text = callback.text
    if not question_text:
        await callback.answer(f"<b><i>Кажется, произошла ошибка.</i></b>\n\nПожалуйста, введите ваш запрос исключительно текстом", parse_mode='HTML')
        return

    profile_link = f'@{callback.from_user.username}'
    group_chat_id = '-4132933387'
    await callback.bot.send_message(group_chat_id, f"<b><i>Пользователь {profile_link} задает вопрос</i></b>:\n<blockquote>{question_text}</blockquote>\n", parse_mode='HTML')
    await callback.answer(f'Вопрос был отправлен сотрудникам на рассмотрение!\n\n<b><i>Помните, что максимальное время ожидания 10 минут!</i></b>', parse_mode='HTML', reply_markup=kb.menu)
    await state.clear()


@router.callback_query(F.data == 'collaboration')
async def get_collaboration(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'<b>Ты попал во вкладку сотрудничества</b>\n\nЕсли у тебя зародилась хорошая идея как ты можешь помочь нам, то смело предлагай ее нам, мы открыты ко всем видам сотрудничества!\n\n<i>Так же у нас есть несколько вакансий!</i><b><i>\n\n-Есть своя идея!\n-Хочу работать с вами!</i></b>', parse_mode='HTML', reply_markup=kb.collaboration)


@router.callback_query(F.data == 'idea')
async def get_idea(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(f'<b>Здесь ты должен описать свою идею, а именно:</b><b><i>\n\n-В чем она заключается?\n-В чем наша выгода?\n-В чем твоя выгода?</i></b>\n\n<i>После всего этого мы рассмотрим твое предложение и ответим тебе!</i>', parse_mode='HTML', reply_markup=kb.collaborationBack)
    await state.set_state(SupportState.waiting_for_idea)


@router.message(SupportState.waiting_for_idea)
async def process_idea_and_send(callback: CallbackQuery, state: FSMContext):
    idea_text = callback.text
    if not idea_text:
        await callback.answer("<b><i>Кажется, произошла ошибка.</i></b>\n\nПожалуйста, введите ваш запрос исключительно текстом", parse_mode='HTML')
        return

    profile_link = f'@{callback.from_user.username}'
    group_chat_id = '-4132933387'
    await callback.bot.send_message(group_chat_id, f"<b><i>У пользователя {profile_link} есть идея</i></b>:\n<blockquote>{idea_text}</blockquote>\n", parse_mode='HTML')
    await callback.answer(f'Заявка была отправлена сотрудникам на рассмотрение!', parse_mode='HTML', reply_markup=kb.menu)
    await state.clear()


@router.callback_query(F.data == 'work')
async def get_application(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(f'<b>Здесь ты должен описать кем ты хочешь быть, а именно:</b><b><i>\n\n-Кем ты себя видишь в DANCE\n-Каковы твои умения?\n-Сколько времени ты готов жертвовать?</i></b>\n\nЗаметь мы развиваемся в разных сферах, мы ищем не только сотрудников, которые будут заниматься только физическим трудом, но и различных творческих людей, таких как:<b><i>\n\n-Программист\n-Дизайнер</i></b>\n\n<i>После всего этого мы рассмотрим твою заявку и ответим тебе!</i>\n\n<b><i>Отправляйте все это одним сообщением, чтобы не нагружать специалистов!</i></b>', parse_mode='HTML', reply_markup=kb.collaborationBack)
    await state.set_state(SupportState.waiting_for_job)


@router.message(SupportState.waiting_for_job)
async def process_work_and_send_application(message: types.Message, state: FSMContext):
    work_text = message.text
    await state.update_data(job=work_text)

    await get_job(message, state)


async def get_job(message: types.Message, state: FSMContext):
    work_text = (await state.get_data()).get('job')
    if not work_text:
        await message.answer(f"<b><i>Кажется, произошла ошибка.</i></b>\n\nПожалуйста, введите ваш запрос исключительно текстом", parse_mode='HTML', reply_markup=kb.collaborationBack)
        return

    user = message.from_user.username
    profile_link = f'@{user}'
    group_chat_id = '-4132933387'
    await message.bot.send_message(group_chat_id, f"<b><i>Пользователь {profile_link} хочет работать с вами</i></b>:\n<blockquote>{work_text}</blockquote>\n", parse_mode='HTML')
    await message.answer(f'Заявка была отправлена сотрудникам на рассмотрение!', parse_mode='HTML',reply_markup=kb.menu)
    await state.clear()


@router.callback_query(F.data == 'aboutUs')
async def get_about(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'<b><i>DANCE - это не просто танец, но и стиль жизни.</i></b>\n<i>Присоединяйся к нам и стань частью этой огромной семьи</i>\n\nКаждый человек, который работает в DANCE, хочет максимально отдастся этому делу, именно поэтому мы стараемся делать все для вас: устраивать лучшие мероприятия, быть отзывчивыми и давать вам множество удобств.\n\n<b>Следите за информацией в нашем телеграмм-канале @dvnce_events</b>\n\n<b>Телеграмм-каналы организаторов:</b><b><i>\n-@ilyhadance\n-@rapispolnitel2006\n-@fuckthischuitsff</i></b>', parse_mode='HTML', reply_markup=kb.menu)
