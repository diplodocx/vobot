import sqlalchemy as db

engine = db.create_engine("sqlite:///english_translater.db")
with engine.connect() as connection:
    metadata = db.MetaData()
    words = db.Table('words', metadata,
                     db.Column('id', db.INTEGER, primary_key=True, autoincrement=True),
                     db.Column('user_id', db.INTEGER),
                     db.Column('en_word', db.TEXT),
                     db.Column('ru_word', db.TEXT))
    # metadata.create_all(engine)
