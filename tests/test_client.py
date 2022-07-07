import pytest

import config.config


@pytest.mark.config
def test_config_valid():
    try:
        import config
        print(config.config.TEST_CONFIG)
    except KeyError as e:
        assert False, "config valid failed"


@pytest.mark.internet
def test_internet_connection():
    import requests
    google = config.config.TEST_INTERNET_URL
    try:
        requests.get(google, timeout=3)
    except Exception as e:
        print(e)
        assert False, 'check internet connection'


@pytest.mark.scrapper
def test_nusorgua():
    from controllers.core.scrapper.scrapper import NusOrgUaParser
    nus = NusOrgUaParser()
    news = nus.get_news()
    assert isinstance(nus.save_news(), list), "news not exists"


@pytest.mark.scrapper
def test_osvita():
    from controllers.core.scrapper.scrapper import OsvitaParser
    osvita = OsvitaParser()
    news = osvita.get_news()
    assert isinstance(osvita.save_news(), list), "news not exists"

