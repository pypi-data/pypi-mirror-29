# encoding: utf-8

import unittest
from stateutil import Switch


class TestSwitch(unittest.TestCase):

    def setUp(self):
        self.sw = Switch(Switch.ON)

    def tearDown(self):
        pass

    def test_switch_on(self):
        self.assertTrue(self.sw.ON)

    def test_switch_off(self):
        self.assertFalse(self.sw.OFF)

    def test_state_on(self):

        self.sw.switch_on()
        state = self.sw.state

        self.assertEqual(self.sw.ON, state, msg=u'Failed to switch on')

    def test_state_off(self):

        self.sw.switch_off()
        state = self.sw.state

        self.assertEqual(self.sw.OFF, state, msg=u'Failed to switch off')


if __name__ == u'__main__':
    unittest.main()
