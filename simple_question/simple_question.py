#!/usr/bin/env python3
import argparse
import logging
import random
from datetime import datetime


from db_schemas import Action, User


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)


class Strategy:
    def __init__(self, args):
        self._args = args

    def process(self):
        raise NotImplementedError(
            '{} does not have process method'.format(
                self.__class__.__name__
            )
        )


class FromStrategy(Strategy):
    action = Action()
    user = User()

    success_messages = [
        'Okay, I have remembered the question from {who} at {at}',
        'Got it! The question was from {who} at {at}',
        'Well, well, well. {who} with question at {at}'
    ]

    def process(self):
        user = self.user.insert(self._args.who)
        self.action.insert(
            what='from',
            user=user,
            at=int(self._args.at.timestamp())
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

    strategy = STRATEGY[args.what](args)
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


