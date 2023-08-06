"""
This will run a series of tests just to ensure the time profile works
It should print out the following answer::

* Note this test is done 10 times to remove timing anomalies
* Note Line number are only included so the test doesn't need to be updated on
    code change
"""
import unittest
import time

from seaborn_timestamp.time_profile import TimeMessage, TimeProfile, sleep
from seaborn_file.file import read_file, relative_path
TimeProfile.SIGNIFICANT_DIGITS = 1 # this is to make the test work
TMI = TimeProfile.message


def basic():
    sleep(1)
    print("Hello World!")


def internal_loop_call_1_15():
    TMI()
    sleep(.1)


@TimeProfile.decorator
def decorator_test_4_6(a, b):
    assert a == 'a' and b == 'b'

    sleep(.4)
    TMI("Message Internal_0 : 10", line_number=206)


def start():
    TMI("Starting 1 : 0", create=True, line_number=209)
    sleep(.1)
    TMI("Next 2 : 1", line_number=211)
    sleep(.2)
    TMI("Start and End 7 : 3", line_number=213)
    sleep(.3)
    decorator_test_4_6('a', b='b')

    TMI("Start and End 7 : 3", done=True, line_number=217)
    sleep(.2)
    for i in range(5):
        TMI("start loop test 1 : 12", line_number=219)
        sleep(.1)
        TMI("next loop test 2 : 13", line_number=221)
        for j in range(3):
            sleep(.2)
            internal_loop_call_1_15()
    TMI("Starting 1", done=True, line_number=225)
    return TimeProfile.report_table()


class TestTimeProfile(unittest.TestCase):
    @unittest.skip("NotImplemented")
    def test_message(self,function=basic,line_number=1, message='test',
                     now=time.time(), thread_start=time.time()):
        msg = TimeMessage(function,line_number,message,now,thread_start)
        return msg

    @unittest.skip("NotImplemented")
    def test_report(self):
        msg = self.test_message()
        self.assertEqual(msg.report(1),{})

    @unittest.skip("NotImplemented")
    def test_update(self):
        msg = self.test_message()
        msg.update(time.time())
        self.assertEqual(1,1)   #TODO: Finish
        return msg

    @unittest.skip("NotImplemented")
    def test_messages(self):
        result = start()
        result.tab = '    '
        doc = globals()['__doc__']
        expected = read_file(relative_path('data/expected_time_profile.txt'))
        print('Time Profile Report:\n%s'%result)
        for i in range(10):
            if str(result) == expected:
                break
            result = start()
        self.assertEqual(expected, str(result))

if __name__ == "__main__":
    unittest.main()
