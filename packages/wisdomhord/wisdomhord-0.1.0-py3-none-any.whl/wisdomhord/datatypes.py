import datetime

class BaseType(object):

    @staticmethod
    def cast_to_hord(value):
        return str(value)

class String(BaseType):

    @staticmethod
    def cast_from_hord(value):
        return value

    @staticmethod
    def cast_to_hord(value):
        return value

class Boolean(BaseType):

    @staticmethod
    def cast_from_hord(value):
        return value == 'True'

    @staticmethod
    def cast_to_hord(value):
        return 'True' if value else 'False'

class Integer(BaseType):

    @staticmethod
    def cast_from_hord(value):
        return int(value)

class Float(BaseType):

    @staticmethod
    def cast_from_hord(value):
        return float(value)

class DateTime(BaseType):

    @staticmethod
    def cast_from_hord(value):
        return datetime.datetime.strptime(value, '%d.%m.%Y // %H.%M.%S')

    @staticmethod
    def cast_to_hord(value):
        return datetime.datetime.strftime(value, '%d.%m.%Y // %H.%M.%S')
