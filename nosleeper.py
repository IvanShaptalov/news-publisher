import datetime
import multiprocessing
import time

from icecream import ic

from config import config


def not_sleeper():
    counter = 0
    while True:
        counter += config.SLEEPER_MINUTES
        print(f'current time: {datetime.datetime.now()}')
        print(f'not sleep for: {counter / 60} hours')
        time.sleep(config.SLEEPER_MINUTES * 60)


if config.SLEEPER:
    not_sleep_thread = multiprocessing.Process(target=not_sleeper)
    not_sleep_thread.start()
    ic('sleeper thread activated')


