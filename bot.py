import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart, CommandObject
import codecs


bot = Bot(token="Ваш токен")  # Объект бота
dp = Dispatcher()  # Диспетчер

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Здравствуйте, это бот для записей на марафоны. \nДля просмотра всего списка команд бота возспользуйтесь /help")

@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer("/help - список всех команд бота"
                         "\n/sign s/m/l ФИО - запись на марафон\n(s - короткие дистанции, m - средние дистанции, l - длинные дистанции)"
                         "\n/search ФИО - записи по ФИО"
                         "\n/list s/m/l - список участников по дистанциям")

@dp.message(Command('sign'))
async def cmd_sign(message: types.Message, command: CommandObject):
    comArgs = command.args.split()
    distanceType = comArgs[0]
    userNameSurname = ' '.join(comArgs[1:])

    if distanceType == 's':
        file = codecs.open('shortlist.txt', 'r', 'utf-8')
        textlist = file.readlines()
        textlist += userNameSurname + '\n'
        file = codecs.open('shortlist.txt', 'w', 'utf-8')
        file.write(''.join(textlist))
        await message.answer(userNameSurname + ", вы успешно записались на короткую дистанцию")
        file.close()
    elif distanceType == 'm':
        file = codecs.open('mediumlist.txt', 'r', 'utf-8')
        textlist = file.readlines()
        textlist += userNameSurname + '\n'
        file = codecs.open('mediumlist.txt', 'w', 'utf-8')
        file.write(''.join(textlist))
        await message.answer(userNameSurname + ", вы успешно записались на среднюю дистанцию")
        file.close()
    elif distanceType == 'l':
        file = codecs.open('longlist.txt', 'r', 'utf-8')
        textlist = file.readlines()
        textlist += userNameSurname + '\n'
        file = codecs.open('longlist.txt', 'w', 'utf-8')
        file.write(''.join(textlist))
        await message.answer(userNameSurname + ", вы успешно записались на длинную дистанцию")
        file.close()
    else:
        await message.answer("Введён неверный аргумент дистанции, выберите один из действительных: s/m/l")

@dp.message(Command('search'))
async def cmd_search(message: types.Message, command: CommandObject):
    comArgs = command.args.split()
    userNameSurname = ' '.join(comArgs)
    findchecker = 0

    file = codecs.open('shortlist.txt', 'r', 'utf-8')
    nameList = file.readlines()
    names = ''.join(nameList)
    if userNameSurname in names:
        await message.answer('Найден ' + userNameSurname + ' в списке на короткую дистанцию')
        findchecker += 1
    file.close()

    file = codecs.open('mediumlist.txt', 'r', 'utf-8')
    nameList = file.readlines()
    names = ''.join(nameList)
    if userNameSurname in names:
        await message.answer('Найден ' + userNameSurname + ' в списке на среднюю дистанцию')
        findchecker += 1
    file.close()

    file = codecs.open('longlist.txt', 'r', 'utf-8')
    nameList = file.readlines()
    names = ''.join(nameList)
    if userNameSurname in names:
        await message.answer('Найден ' + userNameSurname + ' в списке на длинную дистанцию')
        findchecker += 1
    file.close()

    if findchecker == 0:
        await message.answer('По запросу не найдено записей')


@dp.message(Command('list'))
async def cmd_list(message: types.Message, command: CommandObject):
    comArgs = command.args.split()
    distanceType = comArgs[0]

    if distanceType == 's':
        file = codecs.open('shortlist.txt', 'r', 'utf-8')
        await message.answer('Список участников короткой дистанции:\n' + '\n'.join(file.readlines()))
        file.close()
    elif distanceType == 'm':
        file = codecs.open('mediumlist.txt', 'r', 'utf-8')
        await message.answer('Список участников средней дистанции:\n' + '\n'.join(file.readlines()))
        file.close()
    elif distanceType == 'l':
        file = codecs.open('longlist.txt', 'r', 'utf-8')
        await message.answer('Список участников длинной дистанции:\n' + '\n'.join(file.readlines()))
        file.close()
    else:
        await message.answer("Введён неверный аргумент дистанции, выберите один из действительных: s/m/l")


async def botMain():
    await dp.start_polling(bot)