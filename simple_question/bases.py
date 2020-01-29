from datetime import datetime


class Argument:

    def __init__(self, doc, default=None):
        self._value = None
        self._doc = doc
        self._default = default

    def __get__(self, instance, owner):
        if self._default and not self._value:
            return self._default
        return self._value

    def __set__(self, instance, value):
        self._value = value

    def get_doc(self):
        return self._doc


class DateArgument(Argument):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input_formats = [
            '%d-%m-%Y %H:%M',
        ]

    def _parse_input_value(self, value):
        if isinstance(value, datetime):
            return value

        for input_format in self._input_formats:
            try:
                return datetime.strptime(value, input_format)
            except ValueError:        
                pass

        raise ValueError(
            f'{value} does not match any format'
        )

    def __set__(self, instance, value):
        self._value = self._parse_input_value(value)

    def get_doc(self):
        formats = ', '.join(self._input_formats)
        formats = formats.replace('%', '%%')
        return f'{self._doc} //input formats: {formats}'


class ArgumentsMeta(type):

    @staticmethod
    def _declare_arguments(klass, bases, dct):
        klass._declared_arguments = {
            k: v for k, v in dct.items()
            if isinstance(v, Argument)
        }

    def __new__(cls, name, bases, dct):
        klass = super().__new__(cls, name, bases, dct)
        klass._declare_arguments(klass, bases, dct)
        return klass


class Strategy(metaclass=ArgumentsMeta):
 
    def __init__(self, args):
        self._args = args
        self.parse_args(self._args)

    def process(self):
        raise NotImplementedError

    def parse_args(self, args):
        raise NotImplementedError
        
    @classmethod
    def describe_args(cls):
        return ' '.join([
            f.get_doc() for f in 
            cls._declared_arguments.values()
        ])


class WhoWhenParseArgsMixin:
    
    def parse_args(self, args):
        if not args:
             raise ValueError(f'{self} needs at least `who`')

        self.who = args[0]
        if len(args) > 1:
            self.when = args[1]

