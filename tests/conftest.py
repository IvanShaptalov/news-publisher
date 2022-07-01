import datetime
import uuid

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
                inner_id=str(uuid.uuid4()),
                data='some test data in this news',
                source_title='test title',
                news_link='https://test_link',
                source_link='https://test_source_link',
                description='some test description',
                date=datetime.datetime.now())
    return news
