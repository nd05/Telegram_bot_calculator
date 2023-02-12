# Импортируем токен из файла конфигурации
from config import TOKEN
# Импортируем файл с клавиатурами
import keyboards
# Импортируем библиотеку telebot
import telebot
import json
import os
from math import *

# Создаем объект бот 
# Используем токен для подключения бота к телеграмму
bot = telebot.TeleBot(token = TOKEN)

#Переменная, которая будет содержать математическое выражение набраное с калькулятора

users_settings = {}
users = {}

# Добавление пользователя к настройкам 
def add_user(user: telebot.types.User):
    users_settings[str(user.id)] = {'delliting_Ans': True,'calculatin_messages': True,'open_math': False}
    with open(os.path.dirname(os.path.abspath(__file__))+'/users_settings.json', 'w') as file:
        json.dump(users_settings, file,  indent=2, sort_keys=True)

# Проверка настроек пользователя
def check_user(user: telebot.types.User):
    if str(user.id) not in users_settings.keys():
        add_user(user)

# Проверка на нули
def check_for_number(line_of_math: str)-> bool:
    for i in range(len(line_of_math)):
        if line_of_math[len(line_of_math)-1-i] in ['+','-','*','/','(',')']:
            return False
        if line_of_math[len(line_of_math)-1-i] in ['1','2','3','4','5','6','7','8','9']:
            return True
    return False

# Проверка на специальные символоы перед тригонометрией, и если их нет добавление "*"
def times_trigonometry(line_of_math: str)-> str:
    if 'pi' in line_of_math:
        ind= []
        for i in range(len(line_of_math)):
            if not 'p' in line_of_math[0:]:
                break
            if line_of_math[i] == 'p':
                ind.append(i)
        ind.reverse()
        for i in ind:
            if i != 0:
                if not line_of_math[i-1] in ['+','-','*','/','(',')']:
                    line_of_math = line_of_math[:i] + "*" + line_of_math[i:]
    if 'e' in line_of_math:
        ind= []
        for i in range(len(line_of_math)):
            if not 'e' in line_of_math[0:]:
                break
            if line_of_math[i] == 'e':
                ind.append(i)
        ind.reverse()
        for i in ind:
            if i != 0:
                if not line_of_math[i-1] in ['+','-','*','/','(',')']:
                    line_of_math = line_of_math[:i] + "*" + line_of_math[i:]
    if 'sin' in line_of_math:
        ind= []
        for i in range(len(line_of_math)):
            if not 's' in line_of_math[0:]:
                break
            if line_of_math[i] == 's':
                ind.append(i)
        ind.reverse()
        for i in ind:
            if i != 0:
                if not line_of_math[i-1] in ['+','-','*','/','(',')','a']:
                    line_of_math = line_of_math[:i] + "*" + line_of_math[i:]
    if 'cos' in line_of_math:
        ind= []
        for i in range(len(line_of_math)):
            if not 'c' in line_of_math[0:]:
                break
            if line_of_math[i] == 'c':
                ind.append(i)
        ind.reverse()
        for i in ind:
            if i != 0:
                if not line_of_math[i-1] in ['+','-','*','/','(',')','a']:
                    line_of_math = line_of_math[:i] + "*" + line_of_math[i:]
    if 'tan' in line_of_math:
        ind= []
        for i in range(len(line_of_math)):
            if not 't' in line_of_math[0:]:
                break
            if line_of_math[i] == 't':
                ind.append(i)
        ind.reverse()
        for i in ind:
            if i != 0:
                if not line_of_math[i-1] in ['+','-','*','/','(',')','a']:
                    line_of_math = line_of_math[:i] + "*" + line_of_math[i:]
    if 'a' in line_of_math:
        ind= []
        for i in range(len(line_of_math)):
            if not 'a' in line_of_math[0:]:
                break
            if line_of_math[i] == 'a':
                ind.append(i)
        ind.reverse()
        for i in ind:
            if i != 0:
                if not line_of_math[i-1] in ['+','-','*','/','(',')','t']:
                    line_of_math = line_of_math[:i] + "*" + line_of_math[i:]
    return line_of_math

# дебаг строка для тригонометрии
def debug_trigonometry(line_of_math: str)-> str:
    if 's' in line_of_math or 't' in line_of_math:
        print(line_of_math, end=' | ')
        ind= []
        for i in range(len(line_of_math)):
            if not '(' in line_of_math[0:]:
                break
            if line_of_math[i] == '(':
                ind.append(i)
        print(line_of_math, ' | ', ind, sep='')

# Декоратор, который отлавливает события сообщений со знаком /
# тоесть отлавливает команды
@bot.message_handler(commands=['start'])#в аргумент commands пишем отлавливаемую команду 
# Создаем функцию обработчик события отловленного декоратором, что описан на строку выше
def start(message):
    # Отправляем сообщение в чат
    bot.send_message(message.chat.id, # Указывакем id чата для того чтоб 
                                      # бот отправил сообщение в нужный чат
                    "Hi!", # Текст, который выведет бот в сообщение
                    reply_markup = keyboards.mainMenu # Подключаем главную клавиатуру
                    ) 


# Декоратор, который отлавливает события сообщений со знаком /
# тоесть отлавливает команды
@bot.message_handler(commands=['calculator'])# в аргумент commands пишем отлавливаемую команду 
# Создаем функцию обработчик события отловленного декоратором, что описан на строку выше
def calculator(message):
    if not message.chat.id in users.keys():
        users[message.chat.id]= {
            'line_of_math': "",
            'conditional_flags':{
                'new': False,
                'float_number': False,
                'counter_of_*': 0,
                'counter_of_/': 0,
                'no_more_zerro': False,
                'no_more_pi_or_e': False
            }
        }
    check_user(message.chat)
    users[message.chat.id]['line_of_math']= ""
    # Отправляем сообщение в чат
    if not users_settings[str(message.chat.id)]['open_math']:
        # Для людей без тригонометрии
        bot.send_message(message.chat.id, # Указывакем id чата для того чтоб 
                                        # бот отправил сообщение в нужный чат
                        "0", # Текст, который выведет бот в сообщение(0 потому как это начальное знеачение в строке калькулятора)
                        reply_markup = keyboards.calculator # Подключаем клавиатуру-калькулятор
                        )
    else:
        # Для людей c тригонометрией
        bot.send_message(message.chat.id, # Указывакем id чата для того чтоб 
                                        # бот отправил сообщение в нужный чат
                        "0", # Текст, который выведет бот в сообщение(0 потому как это начальное знеачение в строке калькулятора)
                        reply_markup = keyboards.open_calculator # Подключаем клавиатуру-калькулятор
                        )

# Декоратор, который отлавливает события сообщений со знаком /
# тоесть отлавливает команды
@bot.message_handler(commands=['settings'])# в аргумент commands пишем отлавливаемую команду
# Создаем функцию обработчик события отловленного декоратором, что описан на строку выше
def settings(message):
    global users
    global users_settings
    if not message.chat.id in users.keys():
        users[message.chat.id]= {
            'line_of_math': "",
            'conditional_flags':{
                'new': False,
                'float_number': False,
                'counter_of_*': 0,
                'counter_of_/': 0,
                'no_more_zerro': False,
                'no_more_pi_or_e': False
            }
        }
    check_user(message.chat)
    # Отправление сообщения с настройками
    bot.send_message(message.chat.id, # Указывакем id чата для того чтоб 
                                      # бот отправил сообщение в нужный чат
                    "settings:\ndelliting_Ans: " + str(users_settings[str(message.chat.id)]['delliting_Ans'])+"\ncalculatin_messages: " + str(users_settings[str(message.chat.id)]['calculatin_messages']), # Текст, который выведет бот в сообщение с значением настроек
                    reply_markup = keyboards.settings # Подключаем клавиатуру-настроек
                    )

# Переключатель флага для настроек
@bot.callback_query_handler(func=lambda call:call.data in ["xor_delliting_Ans","xor_calculatin_messages"])
# Создаем функцию обработчик события отловленного декоратором, что описан на строку выше
def callback_users_settings_inline(call):
    global users_settings
    # Изменение значения удаления ответов и расчётов сообщений
    if call.data == "xor_delliting_Ans":
        users_settings[str(call.message.chat.id)]['delliting_Ans']= users_settings[str(call.message.chat.id)]['delliting_Ans'] ^ True
    if call.data == "xor_calculatin_messages":
        users_settings[str(call.message.chat.id)]['calculatin_messages']= users_settings[str(call.message.chat.id)]['calculatin_messages'] ^ True
    # Синхронизация изменений с файлом .json
    with open(os.path.dirname(os.path.abspath(__file__))+'/users_settings.json', 'w') as file:
        json.dump(users_settings, file,  indent=2, sort_keys=True)
    # Изменение сообщений для соответствия с изменениями настроек
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="settings:\ndelliting_Ans: " + str(users_settings[str(call.message.chat.id)]['delliting_Ans'])+"\ncalculatin_messages: " + str(users_settings[str(call.message.chat.id)]['calculatin_messages']),reply_markup=keyboards.settings)

# Декоратор отлавливающий callback data
@bot.callback_query_handler(func=lambda call:call.data in [".","=","+","-","*","/","(",")","<=","C","0","1","2","3","4","5","6","7","8","9","pi","e","sin","cos","tan","asin","acos","atan"])
# Создаем функцию обработчик события отловленного декоратором, что описан на строку выше
def callback_inline(call):
    global users
    # Обнуление условий и строки
    if users[call.message.chat.id]['conditional_flags']['new']:
        users[call.message.chat.id]['line_of_math'] = ""
        users[call.message.chat.id]['conditional_flags']['float_number']= False
        users[call.message.chat.id]['conditional_flags']['counter_of_*']= 0
        users[call.message.chat.id]['conditional_flags']['counter_of_/']= 0
        users[call.message.chat.id]['conditional_flags']['no_more_zerro']= True
        users[call.message.chat.id]['conditional_flags']['no_more_pi_or_e']= False
        users[call.message.chat.id]['conditional_flags']['new'] = False

    if call.data == "=":
        # Обрабатываем ошибки при запуске строки users[call.message.chat.id]['line_of_math'] как пайтон кода функцией eval()
        try:
            # Проверка на специальные символоы перед "(", и если их нет добавление "*"
            for i in range(len(users[call.message.chat.id]['line_of_math'])):
                if users[call.message.chat.id]['line_of_math'][i] == "(" and i != 0:
                    # if users[call.message.chat.id]['line_of_math'][i - 1] != "*" and users[call.message.chat.id]['line_of_math'][i - 1] != "+" and users[call.message.chat.id]['line_of_math'][i - 1] != "-" and users[call.message.chat.id]['line_of_math'][i - 1] != "/":
                    # Добавляем знак умножить перед скобкой, если не обнаружено специального символа
                    if not users[call.message.chat.id]['line_of_math'][i-1] in ["-", "+", "/", "*", "n", "s", "g"]:
                        users[call.message.chat.id]['line_of_math'] = users[call.message.chat.id]['line_of_math'][:i] + "*" + users[call.message.chat.id]['line_of_math'][i:]
            # проверка на специальные символы после ")", и если их нет добавление "*"
            for i in range(len(users[call.message.chat.id]['line_of_math'])):
                if users[call.message.chat.id]['line_of_math'][i] == ")" and i != len(users[call.message.chat.id]['line_of_math'])-1:
                    # Добавляем знак умножить после скобки, если не обнаружено специального символа
                    if not users[call.message.chat.id]['line_of_math'][i+1] in ["-", "+", "/", "*", ")"]:
                        users[call.message.chat.id]['line_of_math'] = users[call.message.chat.id]['line_of_math'][:i+1] + "*" + users[call.message.chat.id]['line_of_math'][i+1:]
            # Проверка на совпадение количество скобочек в выражении
            if ("(" in users[call.message.chat.id]['line_of_math']) or (")" in users[call.message.chat.id]['line_of_math']):
                counter_of_openers, counter_of_closers= 0, 0
                for i in users[call.message.chat.id]['line_of_math']:
                    if i == "(":
                        counter_of_openers+= 1
                    if i == ")":
                        counter_of_closers+= 1
                if counter_of_openers-counter_of_closers>0:
                    for i in range(counter_of_openers-counter_of_closers):
                        users[call.message.chat.id]['line_of_math']+= ")"
                if counter_of_openers-counter_of_closers<0:
                    for i in range(counter_of_closers-counter_of_openers):
                        users[call.message.chat.id]['line_of_math']= "(" + users[call.message.chat.id]['line_of_math']
            #debug_trigonometry(users[call.message.chat.id]['line_of_math'])
            users[call.message.chat.id]['line_of_math']= times_trigonometry(users[call.message.chat.id]['line_of_math'])
            #debug_trigonometry(users[call.message.chat.id]['line_of_math'])
            # Вычисление строки
            users[call.message.chat.id]['line_of_math'] = str(eval(users[call.message.chat.id]['line_of_math']))
            # Обнуление счётчиков ответственных за двойную постановку звёздочек и делений
            users[call.message.chat.id]['conditional_flags']['counter_of_*']= 0
            users[call.message.chat.id]['conditional_flags']['counter_of_/']= 0
        # Ошибка деления на ноль
        except ZeroDivisionError:
            users[call.message.chat.id]['line_of_math'] = "Dividing_by_Zerro: Math go brrrr..."
            users[call.message.chat.id]['conditional_flags']['new'] = True
        # Остальные ошибки
        except:
            users[call.message.chat.id]['line_of_math'] = "ERROR"
            users[call.message.chat.id]['conditional_flags']['new'] = True
        # Приведение флага в состоянии True при условии удаления ответа после ввода новых чисел
        if users_settings[str(call.message.chat.id)]['delliting_Ans']:
            users[call.message.chat.id]['conditional_flags']['new'] = True
    # Удаление последнего символа в строке
    elif call.data == "<=":
        users[call.message.chat.id]['line_of_math'] = users[call.message.chat.id]['line_of_math'][:len(users[call.message.chat.id]['line_of_math'])-1]
        if len(users[call.message.chat.id]['line_of_math']) == 0:
            users[call.message.chat.id]['line_of_math'] = "0"
            users[call.message.chat.id]['conditional_flags']['new'] = True
    # Удалении строки
    elif call.data == "C":
        users[call.message.chat.id]['line_of_math'] = "0"
        users[call.message.chat.id]['conditional_flags']['new'] = True
    
        
    elif call.data:
        # Сохраняем 0 в случае, если первым симворлом пользователь ввел символ "."
        if users[call.message.chat.id]['line_of_math'] == "" and call.data == ".":
            users[call.message.chat.id]['line_of_math'] = "0"
        # удаление нуля перед символами и установка флага на False
        if call.data in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/',"pi","e","sin","cos","tan","asin","acos","atan"]:
            if users[call.message.chat.id]['conditional_flags']['no_more_zerro']:
                users[call.message.chat.id]['line_of_math']= users[call.message.chat.id]['line_of_math'][:len(users[call.message.chat.id]['line_of_math'])-1]
            users[call.message.chat.id]['conditional_flags']['no_more_zerro']= False
        # Отключение точки при попытке повторной установки в дробное число, отключение специальных символов за исключением минуса если строка в себе не содержит чисел, выключение чисел после pi и e
        if (call.data == "." and users[call.message.chat.id]['conditional_flags']['float_number']) or ((call.data in ["+", "*", "/"]) and len(users[call.message.chat.id]['line_of_math'])==0) or (not call.data in ['+', '-', '*', '/', '(',')'] and users[call.message.chat.id]['conditional_flags']['no_more_pi_or_e']):
            return
        # Выключение нуля при условии превышения количества нулей разрешенных для ввода в условиях
        # Подсчет количества звёздочек и делений для органичения по количеству до двух
        if call.data == "*":
            users[call.message.chat.id]['conditional_flags']['counter_of_*']+= 1
        if call.data == "/":
            users[call.message.chat.id]['conditional_flags']['counter_of_/']+= 1
        if (call.data in ["*", "/"]) and (users[call.message.chat.id]['conditional_flags']['counter_of_*']>=3 or users[call.message.chat.id]['conditional_flags']['counter_of_/']>=3):
            return
        # Установка флага на дробность числа
        if call.data == "." and (not users[call.message.chat.id]['conditional_flags']['float_number']):
            # добавление нуля при постановке точки после символов действий
            if users[call.message.chat.id]['line_of_math'][-1] in ["+", "-", "*", "/"]:
                users[call.message.chat.id]['line_of_math']+= "0"
            users[call.message.chat.id]['conditional_flags']['float_number']= True
            users[call.message.chat.id]['conditional_flags']['no_more_zerro']= False
        # Удаление флага на дробность числа
        if call.data in ["+", "-", "*", "/", "(", ")"]:
            users[call.message.chat.id]['conditional_flags']['float_number']= False
            users[call.message.chat.id]['conditional_flags']['no_more_pi_or_e']= False
        # установление флага на pi и e
        if call.data in ['pi', 'e']:
            users[call.message.chat.id]['conditional_flags']['no_more_pi_or_e']= True
        # Запрет на ввод нуля
        if not(call.data == "0" and users[call.message.chat.id]['conditional_flags']['no_more_zerro']): 
            if call.data == '0' and not users[call.message.chat.id]['conditional_flags']['float_number']:
                if not check_for_number(users[call.message.chat.id]['line_of_math']):
                    users[call.message.chat.id]['conditional_flags']['no_more_zerro']= True
            # добавление call.data
            users[call.message.chat.id]['line_of_math'] = users[call.message.chat.id]['line_of_math'] + call.data
    # изменение сообщеня калькулятора
    if call.message.text != users[call.message.chat.id]['line_of_math'] and users[call.message.chat.id]['line_of_math'] != "":
        if call.data in ["sin","cos","tan","asin","acos","atan"]:
            users[call.message.chat.id]['line_of_math']+= '('
        # версия для пользователей с открытой математикой и нет
        if users_settings[str(call.message.chat.id)]['open_math']:
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = users[call.message.chat.id]['line_of_math'], reply_markup=keyboards.open_calculator)
        else:
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = users[call.message.chat.id]['line_of_math'], reply_markup=keyboards.calculator)

#Вычисление сообщений
@bot.message_handler(content_types=['text'])
def dialog_message(message):
    global users
    global users_settings
    if not message.chat.id in users.keys():
        users[message.chat.id]= {
            'line_of_math': "",
            'conditional_flags':{
                'new': False,
                'float_number': False,
                'counter_of_*': 0,
                'counter_of_/': 0,
                'no_more_zerro': False,
                'no_more_pi_or_e': False
            }
        }
    check_user(message.chat)
    users[message.chat.id]['line_of_math']= ""
    if message.text == "λ=open_math":
        users_settings[str(message.chat.id)]['open_math']= True
        bot.send_message(message.chat.id,"Math_opened",reply_markup = keyboards.mainMenu)
        with open(os.path.dirname(os.path.abspath(__file__))+'/users_settings.json', 'w') as file:
            json.dump(users_settings, file,  indent=2, sort_keys=True)
    if message.text == "λ=close_math":
        users_settings[str(message.chat.id)]['open_math']= False
        bot.send_message(message.chat.id,"Math_closed",reply_markup = keyboards.mainMenu)
        with open(os.path.dirname(os.path.abspath(__file__))+'/users_settings.json', 'w') as file:
            json.dump(users_settings, file,  indent=2, sort_keys=True)
    if not users_settings[str(message.chat.id)]['calculatin_messages']:
        return
    elif message.text[0] == "=":
        line_of_math= message.text[1:]
        try:
            # Проверка на специальные символоы перед "(", и если их нет добавление "*"
            for i in range(len(line_of_math)):
                if line_of_math[i] == "(" and i != 0:
                    # if line_of_math[i - 1] != "*" and line_of_math[i - 1] != "+" and line_of_math[i - 1] != "-" and line_of_math[i - 1] != "/":
                    # Добавляем знак умножить перед скобкой, если не обнаружено специального символа
                    if not line_of_math[i-1] in ["-", "+", "/", "*", "n", "s", "g"]:
                        line_of_math = line_of_math[:i] + "*" + line_of_math[i:]
            # проверка на специальные символы после ")", и если их нет добавление "*"
            for i in range(len(line_of_math)):
                if line_of_math[i] == ")" and i != len(line_of_math)-1:
                    # Добавляем знак умножить после скобки, если не обнаружено специального символа
                    if not line_of_math[i+1] in ["-", "+", "/", "*", ")"]:
                        line_of_math = line_of_math[:i+1] + "*" + line_of_math[i+1:]
            # Проверка на совпадение количество скобочек в выражении
            if ("(" in line_of_math) or (")" in line_of_math):
                counter_of_openers, counter_of_closers= 0, 0
                for i in line_of_math:
                    if i == "(":
                        counter_of_openers+= 1
                    if i == ")":
                        counter_of_closers+= 1
                if counter_of_openers-counter_of_closers>0:
                    for i in range(counter_of_openers-counter_of_closers):
                        line_of_math+= ")"
                if counter_of_openers-counter_of_closers<0:
                    for i in range(counter_of_closers-counter_of_openers):
                        line_of_math= "(" + line_of_math
            while ',' in line_of_math:
                line_of_math= line_of_math[:line_of_math.index(',')]+'.'+line_of_math[line_of_math.index(',')+1:]
            #debug_trigonometry(line_of_math)
            line_of_math= times_trigonometry(line_of_math)
            #debug_trigonometry(line_of_math)
            # Вычисление строки
            line_of_math = str(eval(line_of_math))
            # Обнуление счётчиков ответственных за двойную постановку звёздочек и делений
        except ZeroDivisionError:
            line_of_math = "Dividing_by_Zerro: Math go brrrr..."
        except:
            line_of_math = "ERROR"
        bot.send_message(message.chat.id, line_of_math)

# Комада, которая запускает отлавливание сообщений в чат

if __name__ == "__main__":
    try:
        with open(os.path.dirname(os.path.abspath(__file__))+'/users_settings.json') as file:
            users_settings = json.load(file)
    except:
        users_settings = {"0": {}}
        with open(os.path.dirname(os.path.abspath(__file__))+'/users_settings.json', 'w') as file:
            json.dump(users, file,  indent=2, sort_keys=True)
    bot.polling(none_stop = True)
    # написать комментарий к функциям