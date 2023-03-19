import sqlalchemy as db
from create_tables import words

engine = db.create_engine("sqlite:///english_translater.db")
connection = engine.connect()


def insert_data(data_dict):
    insertion_query = words.insert().values([data_dict])
    connection.execute(insertion_query)
    connection.commit()


def delete_word(user_id, word, lang):
    if lang == 'en':
        delete_query = db.delete(words).where(words.columns.user_id == user_id).where(words.columns.en_word == word)
    else:
        delete_query = db.delete(words).where(words.columns.user_id == user_id).where(words.columns.ru_word == word)
    connection.execute(delete_query)
    connection.commit()


def return_list(user_id):
    select_all_query = db.select(words.columns.en_word, words.columns.ru_word).where(words.columns.user_id == user_id)
    result = connection.execute(select_all_query)
    return result.fetchall()


def return_ordered_list(user_id):
    select_all_query = db.select(words.columns.en_word, words.columns.ru_word).where(words.columns.user_id == user_id) \
        .order_by(words.columns.en_word)
    result = connection.execute(select_all_query)
    return result.fetchall()
