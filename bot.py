from telebot import TeleBot
from translater import translate_word_to_russian, translate_word_to_english, define_language
import logging
from data_producing import insert_data, delete_word, return_list, return_ordered_list
import random

token = "6126729690:AAEyzxmPGPdtjxaQlJ3IHQs2yektnEZefPs"
bot = TeleBot(token)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


@bot.message_handler(commands=['start'])
def on_start(message):
    bot.send_message(message.chat.id, "hello! What is your naaaaame?")


def separate(message):
    raw_text = message.text.split()
    command = raw_text[0]
    text_to_translate = raw_text[1:]
    text = ' '.join(text_to_translate)
    return text.strip(), command


def list_to_str(list):
    str_list = []
    for tuple in list:
        str_list.append(' - '.join(tuple))
    res = '\n'.join(str_list)
    return res


def on_translate(message, method, lang='en'):
    text, command = separate(message)
    translated_text = method(text)
    # logger.debug(translated_text)
    bot.send_message(message.chat.id, translated_text)
    if command == "/tte":
        en_word = translated_text
        ru_word = text
    elif command == "/ttr":
        en_word = text
        ru_word = translated_text
    else:
        if lang == 'en':
            en_word = translated_text
            ru_word = text
        else:
            en_word = text
            ru_word = translated_text
    data_dict = {'user_id': message.from_user.id, 'en_word': en_word, 'ru_word': ru_word}
    insert_data(data_dict)


@bot.message_handler(commands=['ttr'])
def on_translate_to_russian(message):
    on_translate(message, translate_word_to_russian, lang='ru')


@bot.message_handler(commands=['tte'])
def on_translate_to_english(message):
    on_translate(message, translate_word_to_english, lang='en')


@bot.message_handler(commands=['a'])
def on_adding(message):
    text, command = separate(message)
    language = define_language(text)
    if language:
        if language == 'ru':
            on_translate_to_english(message)
        else:
            on_translate_to_russian(message)
    else:
        bot.send_message(message.chat.id, "Wrong request, try /tte or /ttr")


def on_delete(message, language):
    text, command = separate(message)
    delete_word(message.from_user.id, text, language)
    bot.send_message(message.chat.id, "Удаление")


@bot.message_handler(commands=['de'])
def on_delete_english(message):
    on_delete(message, 'en')


@bot.message_handler(commands=['dr'])
def on_delete_russian(message):
    on_delete(message, 'ru')


def on_select(message, method):
    list = method(message.from_user.id)
    text = list_to_str(list)
    # logger.debug(text)
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['l'])
def on_simple_select(message):
    on_select(message, return_list)


@bot.message_handler(commands=['ol'])
def on_ordered_select(message):
    on_select(message, return_ordered_list)


@bot.message_handler(commands=['tm'])
def on_test_me(message):
    data_list = return_list(message.from_user.id)
    # logger.debug(data_list)
    random.shuffle(data_list)
    random_tuple = list(data_list[0])
    random.shuffle(random_tuple)
    origin, translation = random_tuple
    bot.send_message(message.chat.id, f"{origin} ||{translation}||", parse_mode='MarkdownV2')


bot.infinity_polling()
