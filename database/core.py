from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.config import DB_URL, ECHO, TEST_DB_URL

engine = create_engine(DB_URL,
                       echo=ECHO)
test_engine = create_engine(TEST_DB_URL,
                            echo=ECHO)

db_session = sessionmaker(bind=engine)()
receiver_db_session = sessionmaker(bind=engine)()

test_db_session = sessionmaker(bind=test_engine)()

Base = declarative_base()

