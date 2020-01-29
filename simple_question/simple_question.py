#!/usr/bin/env python3
import argparse
import logging
import random
from datetime import datetime
from matplotlib import pyplot


from db_schemas import (
    Action, 
    User
)
from bases import (
    Argument, 
    DateArgument, 
    Strategy,
    WhoWhenParseArgsMixin,

)


logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(), ]
)


class FromStrategy(WhoWhenParseArgsMixin, Strategy):
    who = Argument('`who` (diverted you)')
    when = DateArgument(
        '`when` (it happend)',
        default=datetime.now()
    )

    action = Action()
    user = User()

    success_messages = [
        'Okay, I have remembered the question from {who} at {at}',
        'Got it! The question was from {who} at {at}',
        'Well, well, well. {who} with question at {at}'
    ]

    def process(self):
        user = self.user.insert(self.who)
        self.action.insert(
            what='from',
            user=user,
            at=int(self.when.timestamp())
        )
        logging.info(
            random.choice(self.success_messages).format(
                who=self.who,
                at=self.when
            )
        )


class ToStrategy(WhoWhenParseArgsMixin, Strategy):
    who = Argument('`who` (you diverted)')
    when = DateArgument(
        '`when` (it happend)',
        default=datetime.now()
    )

    action = Action()
    user = User()

    def process(self):
        user = self.user.insert(self.who)
        self.action.insert(
            what='to',
            user=user,
            at=int(self.when.timestamp())
        )
        logging.info(
            f'Oks, question from you to {self.who} at {self.when}'
        )


class VisualizeStrategy(Strategy):
    whose = Argument(
        '`whose` (question are you interested)', 
        default='all'
    )

    def parse_args(self, args):
        self.whose = args[0]

    def process(self):
        figure = pyplot.figure()
        figure.suptitle('questions')
        figure.show('img.svg')


STRATEGY = {
    'from': FromStrategy,
    'to': ToStrategy,
    'show': VisualizeStrategy
}


def simple_question():
    args = init_arguments()

    strategy = STRATEGY[args.what](args.args)
    strategy.process()


def get_args_description():
    commands = [
        f'{what} {s.describe_args()}' 
        for what, s in STRATEGY.items()
    ]
    return '\n'.join(commands)
 

def init_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'what', 
        type=str,
    )
    parser.add_argument(
        'args', 
        type=str, 
        nargs='+',
        help=get_args_description()
    )
    return parser.parse_args()


if __name__ == '__main__':
    simple_question()


