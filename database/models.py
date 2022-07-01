import datetime

from icecream import ic
from sqlalchemy import Column, String, ForeignKey, DateTime

from config import config
from database import db_methods
from database.core import Base
from database.db_methods import write_obj_to_table, delete_obj_from_table


class Dictionable:
    attrs_to_save = ()

    def to_dict(self):
        result = {}
        for attr in self.attrs_to_save:
            result[attr] = self.__getattribute__(attr)
        return result


class News(Base):
    __tablename__ = 'news'

    inner_id = Column('inner_id', String, unique=True, primary_key=True, index=True)
    news_id = Column('news_id', String, unique=False)
    data = Column('data', String, unique=False)
    source_title = Column('source_title', String, unique=False)
    source_link = Column('source_link', String, unique=False)
    news_link = Column('source_link', String, unique=False)
    description = Column('description', String, unique=False)
    date = Column('date', DateTime, unique=False, nullable=True)
    telegram_news_id = Column('telegram_news_id', String, unique=False, nullable=False)

    attrs_to_save = ('news_id',
                     'inner_id',
                     'data',
                     'source_title',
                     'source_link'
                     'news_link',
                     'description',
                     'date',
                     'telegram_news_id')

    @staticmethod
    def get_from_db(open_session, news_id):
        result_news = db_methods.get_from_db_multiple_filter(table_class=News,
                                                             identifier_to_value=[News.news_id == news_id],
                                                             open_session=open_session)

        return result_news

    @staticmethod
    def paginate(open_session, start_date, end_date, per_page, page_number):
        raw_news_list = open_session.query(News). \
            filter(*[News.date >= start_date, News.date <= end_date]) \
            .limit(per_page). \
            offset((page_number - 1) * per_page).all()

        news_list = []

        news_list += [news.to_dict(format_date=True) for news in raw_news_list]
        return news_list

    def to_dict(self, format_date=False):
        result = {}
        for attr in self.attrs_to_save:
            result[attr] = self.__getattribute__(attr)
            if isinstance(self.__getattribute__(attr), datetime.datetime) and format_date:
                result[attr] = self.__getattribute__(attr).strftime(config.TIME_FORMAT)
        return result

    def save(self, open_session, identifier_to_value=None):
        if identifier_to_value is None:
            identifier_to_value = [News.news_id == self.news_id]
        print('write')
        write_obj_to_table(open_session=open_session,
                           table_class=News,
                           identifier_to_value=identifier_to_value,
                           **self.to_dict())

    def delete(self, open_session):
        try:
            return delete_obj_from_table(open_session=open_session,
                                         table_class=News,
                                         identifier_to_value=[News.news_id == self.news_id])
        except Exception as e:
            print(e)
            return False

    def __str__(self):
        return f'{self.date} {self.description}'


def create_tables(c_engine):
    Base.metadata.create_all(bind=c_engine)
    ic('tables created')
    return True


def drop_tables(c_engine):
    Base.metadata.drop_all(bind=c_engine)
    ic('tables deleted')
    return True
