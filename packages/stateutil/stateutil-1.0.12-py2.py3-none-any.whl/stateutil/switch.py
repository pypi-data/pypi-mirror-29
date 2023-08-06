# encoding: utf-8


class Switch(object):

    ON = True
    OFF = False

    def __init__(self,
                 state=OFF):

        self._state = True if state else False

    def switch_on(self):
        self._state = True
        self._switch_on_action()

    def _switch_on_action(self):
        u"""
        Override this method to take action when the
        state of a switch changes to on
        """
        pass

    def switch_off(self):
        self._state = False
        self._switch_off_action()

    def _switch_off_action(self):
        u"""
        Override this method to take action when the
        state of a switch changes to off
        """
        pass

    def state_change(self):
        self.switch_off() if self.switched_on else self.switch_on()

    def __nonzero__(self):
        return self._state

    @property
    def state(self):
        return self.ON if self._state else self.OFF

    @state.setter
    def state(self,
              state):
        self._state = self.ON if state else self.OFF

    @property
    def switched_on(self):
        return self.state == self.ON

    @property
    def switched_off(self):
        return self.state == self.OFF
