import configparser
import os
import re
from pathlib import Path

base_dir = Path(__file__).resolve().parent
settings = configparser.ConfigParser()
print(base_dir)
settings.read(os.path.join(base_dir, "config.ini"))


def database_link(test=False):
    if test:
        pre_database_url = os.environ.get('HEROKU_POSTGRESQL_AMBER_URL') or settings['DATABASE']['TEST_URL']
    else:
        pre_database_url = os.environ.get('DATABASE_URL') or settings['DATABASE']['URL']
    print(pre_database_url.replace(pre_database_url[pre_database_url.index('//'):pre_database_url.index('@')], '*' * 3))
    if pre_database_url is None:
        raise ValueError('db url is None')
    arr = re.split(pattern=r'[:|@|/]', string=pre_database_url)
    while '' in arr:
        arr.remove('')
    if arr and len(arr) == 6:
        name = arr[5]
        print(name)
        print('info from arr ', len(arr))
        user = arr[1]
        password = arr[2]
        host_db = arr[3]
        port = arr[4]
        db_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(user, password, host_db, name)
        return db_path
    return pre_database_url


DB_URL = database_link()
TEST_DB_URL = database_link(test=True)

ECHO = str(os.environ.get('DB_ECHO')) == '1' or settings.getboolean(section='DATABASE',
                                                                    option='ECHO')

TIME_FORMAT = '%d.%m.%Y'

SLEEPER = str(os.environ.get('SLEEPER')) == '1' or str(settings['SYSTEM']['SLEEPER']) == '1'
SLEEPER_MINUTES = os.environ.get('SLEEPER_MINUTES') or settings['SYSTEM']['SLEEPER_MINUTES']
SLEEPER_MINUTES = int(SLEEPER_MINUTES)
TEST_INTERNET_URL = os.environ.get('TEST_INTERNET_URL') or settings['TEST']['INTERNET_URL']

GROUP_MAIN_ID = os.environ.get('MAIN_GROUP_ID') or settings['GROUPS']['MAIN_ID']
GROUP_EDIT_ID = os.environ.get('EDIT_GROUP_ID') or settings['GROUPS']['EDIT_ID']
GROUP_PHOTOS_ID = os.environ.get('PHOTOS_GROUP_ID') or settings['GROUPS']['PHOTOS_ID']

TEST_CONFIG = 'ok'  # must be on last line
