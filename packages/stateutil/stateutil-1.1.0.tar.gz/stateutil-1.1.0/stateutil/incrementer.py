# encoding: utf-8


class Incrementer(object):

    def __init__(self,
                 start_value=0,
                 increment=1):
        self.__start_value = start_value
        self.__max = start_value
        self.__increment = increment
        self.set(start_value)

    def prev(self,
             increment=None):
        self.__count -= increment if increment else self.__increment
        return self.__count

    def previous(self,
                 increment=None):
        return self.prev(increment)

    def __set_max(self):
        if self.__count > self.__max:
            self.__max = self.__count

    def set(self,
            value):
        self.__count = value
        self.__set_max()

    @property
    def max(self):
        return self.__max

    def next(self,
             increment=None):
        self.__count += increment if increment else self.__increment
        self.__set_max()
        return self.__count

    def start(self):
        self.__count = self.__start_value
        return self.__count

    @property
    def current(self):
        return self.__count
