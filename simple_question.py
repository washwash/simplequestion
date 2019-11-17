#!/usr/bin/env python3
import argparse
import logging
import sqlite3
import random
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)


class DB:
    class manager:
        def __init__(self):
            self.conn = sqlite3.connect('sq.db')
            self.cursor = self.conn.cursor()

        def __enter__(self):
            return self

        def __exit__(self, type, value, traceback):
            self.conn.close()

        def execute(self, sql):
            self.cursor.execute(sql)
            self.conn.commit()

    def __init__(self):
        with self.manager() as m:
            m.execute(
                '''
                CREATE TABLE IF NOT EXISTS "sq.actions" (
                    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "what" TEXT,
                    "who" TEXT,
                    "at" REAL
                );
                '''
            )

    def execute(self, sql):
        with self.manager() as m:
            m.execute(sql)


class Strategy:
    def __init__(self, args, db):
        self._args = args
        self._db = db

    def process(self):
        raise NotImplementedError(
            '{} does not have process method'.format(
                self.__class__.__name__
            )
        )


class FromStrategy(Strategy):

    success_messages = [
        'Okay, I have remembered the question from {who} at {at}',
        'Got it! The question was from {who} at {at}',
        'Well, well, well. {who} with question at {at}'
    ]

    def process(self):
        self._db.execute(
            '''
            INSERT INTO "sq.actions" ("what", "who", "at")
            VALUES ("from",  "{who}", "{at}");
            '''.format(
                who=self._args.who,
                at=self._args.at
            )
        )
        logging.info(
            random.choice(self.success_messages).format(
                who=self._args.who,
                at=self._args.at
            )
        )


class ToStrategy(Strategy):

    def process(self):
        logging.info('To st')


STRATEGY = {
    'from': FromStrategy,
    'to': ToStrategy
}


def simple_question():
    args = init_arguments()

    strategy = STRATEGY[args.what](args, DB())
    strategy.process()


def init_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'what', type=str
    )
    parser.add_argument(
        'who', type=str
    )
    parser.add_argument(
        '-at',
        default=datetime.now(),
        required=False
    )
    return parser.parse_args()


if __name__ == '__main__':
    simple_question()


