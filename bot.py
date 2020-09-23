import telebot
import output_taker

file_name = 'token.txt'

with open(file_name, mode='r') as file:
    token = file.read()

if token is None or token == '':
    print('There\'s no token')
    exit()

bot = telebot.TeleBot(token)
client_status = {}


@bot.message_handler(commands=['help'])
def help_com(message):
    client_status[message.from_user.id] = None
    bot.send_message(message.from_user.id, "Now there are following commands:\n\n "
                                           "/repeat (+word) to make me repeat what you said\n"
                                           "/code to execute python code\n"
                                           "/say_hi to make me to say hi to you\n"
                                           "/help to watch commands list\n\n"
                                           "Have a nice day!")


@bot.message_handler(commands=['repeat'])
def repeat(message):
    try:
        client_status[message.from_user.id] = None
        bot.send_message(message.from_user.id, message.text[7:])
    except BaseException:
        client_id = message.from_user.id
        client_status[client_id] = 'wait_for_word'
        bot.send_message(message.from_user.id, 'Write the word I should repeat')


@bot.message_handler(commands=['say_hi'])
def say_hi(message):
    client_status[message.from_user.id] = None
    bot.send_message(message.from_user.id, "Hi {} nice to meet you".format(message.from_user.first_name))


@bot.message_handler(commands=['code'])
def info_code(message):
    client_id = message.from_user.id
    client_status[client_id] = 'wait_for_code'
    bot.send_message(message.from_user.id, 'Send me your code')


@bot.message_handler(content_types=['text'])
def exe(message):
    client_id = message.from_user.id

    if client_id in client_status and client_status[client_id] == 'wait_for_code':
        run_code(message)

    elif client_id in client_status and client_status[client_id] == 'wait_for_word':
        bot.send_message(message.from_user.id, message.text)

    else:
        print(message.text)
        bot.send_message(message.from_user.id,
                         "Hi {}. Type /help to see commands"
                         .format(message.from_user.first_name))


def run_code(message):
    output = []

    code = message.text
    print("Code is: \n" + code)

    try:
        with output_taker.OutputInterceptor() as output:
            exec(code)

    except BaseException as error:
        output = ['Something went wrong',
                  error]

    finally:
        result = '\n'.join(output)

    if result != '':
        try:
            bot.send_message(message.from_user.id, result)

        except BaseException:
            bot.send_message(message.from_user.id,
                             'Seems like I can not send a message\n'
                             'maybe its too heavy for me\n'
                             'please check your code')
    else:
        bot.send_message(message.from_user.id, "Did it")


bot.polling(none_stop=True, interval=0)
