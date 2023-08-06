#!/usr/bin/env python

import time
import random
import sys
import json
import logging

from faker import Faker

fake = Faker()

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'FATAL', ]
NAMES = fake.words(nb=random.randint(3, 6))

def random_path(min_dirs=1, max_dirs=10):
    n_dirs = random.randint(1, 10)
    return '/' + '/'.join(fake.words(nb=n_dirs)).lower()

def random_level(n):
    return LOG_LEVELS[n]

def random_level_number(n):
    return [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
            logging.FATAL][n]

def fake_word():
    return fake.words(nb=1)[0]

def random_message():
    """ Log messages can sometimes be sperated with 'message' and 'args',
    so show what a log message would look like in that instance.
    """
    placeholders_n = random.randint(0, 5)
    placeholder_values = fake.words(nb=placeholders_n)
    message = []
    i = 0
    while i < placeholders_n:
        if random.randint(0, 4) <= 3:
            message.append(fake_word())
        else:
            message.append('%s')
            i += 1
    return (' '.join(message), placeholder_values)

def random_log_output():
    log_level_n = random.randint(0, len(LOG_LEVELS)-1)
    (msg, args) = random_message()
    return {
      "name": random.choice(NAMES),
      "msg": msg,
      "args": tuple(args),
      "levelname": random_level(log_level_n),
      "levelno": str(random_level_number(log_level_n)),
      "pathname": random_path(),
      "filename": fake.file_name(extension='py'),
      "module": fake_word(),
      "exc_info": "None",
      "exc_text": "None",
      "stack_info": "None",
      "lineno": str(fake.pyint()),
      "funcName": fake_word(),
      "created": str(fake.pyfloat(left_digits=10, right_digits=8, positive=True)),
      "msecs": str(fake.pyfloat(left_digits=3, right_digits=12, positive=True)),
      "relativeCreated": str(fake.pyfloat(left_digits=3, right_digits=12, positive=True)),
      "thread": str(fake.random_number(digits=12)),
      "threadName": "MainThread",
      "processName": "MainProcess",
      "process": "16475",
    }

while 1:
    print(json.dumps(random_log_output(), indent=2))
    time.sleep(fake.pyfloat(left_digits=0))
