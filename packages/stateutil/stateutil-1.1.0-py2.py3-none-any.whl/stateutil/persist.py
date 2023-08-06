# encoding: utf-8

import json
from classutils.observer import ObservableMixIn


class Persist(ObservableMixIn):

    """
    Add a key value pair to persistent storage
    e.g. to a database table given appropriate methods.

    The 'persistent store' needs to implement __getitem__ and __setitem__.
    """

    INITIAL_VALUE = u''

    def __init__(self,
                 persistent_store,
                 key,
                 initial_value=None):
        """
        :param persistent_store: An object that gives access to the persistent
                                 store. It should implement __getitem__, raising
                                 KeyError if the item is not found. It should

        :param key: Name of thing we are storing, e.g. username
        :param initial_value: Set this value in the persistent store if it's
                              not there already
        """
        self.persistent_store = persistent_store
        self.key = key
        self.initial_value = (self.INITIAL_VALUE
                              if initial_value is None
                              else initial_value)

    @staticmethod
    def encode(value):
        """
        Overload this if you need to modify the value before storing
        e.g. Pickle
        """
        return value

    @staticmethod
    def decode(value):
        """
        Overload this if you need to modify the value after retrieving
        e.g. Unpickle
        """
        return value

    def __getitem__(self,
                    item):
        # Required to use nested Persist objects
        value = self.persistent_store[self.key]
        return value

    def set(self,
            value):
        self.persistent_store[self.key] = self.encode(value)
        self.notify_observers(key=self.key,
                              value=value)

    def get(self):
        try:
            return self.decode(self.persistent_store[self.key])
        except KeyError:
            self.set(self.initial_value)
            return self.initial_value

    @property
    def value(self):
        return self.get()

    @value.setter
    def value(self,
              value):
        self.set(value)


class PersistJSON(Persist):

    INITIAL_VALUE = {}

    @staticmethod
    def encode(value):
        return json.dumps(value)

    @staticmethod
    def decode(value):
        return json.loads(value)
