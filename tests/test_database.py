import pytest
from database.core import test_db_session
from database.models import News


@pytest.mark.database
def test_database_news_saving_deleting(news):
    try:
        with test_db_session as s:
            news.save(s)
            news_dict = news.to_dict()
            result_news = News.get_from_db(open_session=s,
                                           news_id=news.news_id)

            assert isinstance(result_news, News)
            result_news_dict = result_news.to_dict()
            assert news_dict == result_news_dict

            result_news.delete(open_session=s)

            none_news = News.get_from_db(open_session=s,
                                         news_id=news.news_id)
            assert none_news is None
    except Exception as e:
        raise e
    finally:
        test_db_session.rollback()

