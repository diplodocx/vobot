from googletrans import Translator

translator = Translator()


def translate_to_any(old_word, src, dest):
    translated = translator.translate(old_word, src=src, dest=dest)
    new_word = translated.text
    return new_word


def translate_word_to_russian(old_word):
    return translate_to_any(old_word, src='en', dest='ru')


def translate_word_to_english(old_word):
    return translate_to_any(old_word, src='ru', dest='en')


def define_language(text):
    language = translator.detect(text).lang
    if language in ('ru', 'en'):
        return language
    else:
        return None