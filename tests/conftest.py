import datetime

import pytest
from icecream import ic

import config.config
from database.core import test_engine
from database.models import News


@pytest.fixture
def tables_drop():
    ic(config.config.TEST_DB_URL)
    from database.models import drop_tables
    assert drop_tables(test_engine), "tables not dropped"


@pytest.fixture()
def tables_creating(tables_drop):
    ic(config.config.TEST_DB_URL)
    from database.models import create_tables
    assert create_tables(test_engine), "tables not created"
    return True


@pytest.fixture
def news(tables_creating) -> News:
    news = News(news_id='19',
                text='text',
                telegram_news_id='123123',
                source_title='test title',
                news_link='https://test_link',
                source_link='https://test_source_link',
                telegram_news_id_edit='1231232',
                date=datetime.datetime.now())
    return news
