'''RTool/time.py

This module is used for extended functionality of the default time
package in Python.  For now it only holds a Stopwatch class used to
get run time.

Example:
    The stopwatch class is meant to be used inline. You can start
    the stopwatch as so::

        $ stopwatch = Stopwatch()

    Then you can print the elapsed time by doing the following::

        $ stopwatch.stop()

    Or return the current time (formatted) as string::

        $ example_string = stopwatch.current()
        $ print(example_string)

'''

from __future__ import absolute_import
import time

class Stopwatch():
    '''The Stopwatch class.

    'Stopwatch' is used inline to get the elapsed time since creation
    of the Stopwatch object.

    Look at module docstrings for example of usage.

    Notes:
        The stop() method does not actually stop the Stopwatch. The
        Stopwatch object is only active when called so there is no need
        to worry about it continuing to run after you are done with it.
    '''
    def __init__(self):
        self.initialTime = 0
        self.totalTime = 0
        self.start()
    def start(self):
        self.initialTime = time.time()
    def stop(self):
        self.totalTime = time.time() - self.initialTime
        print(self.getFormattedTime(self.totalTime))
    def current(self):
        totalTime = time.time() - self.initialTime
        return self.getFormattedTime(totalTime)
    def getFormattedTime(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return("%d:%02d:%02d"%(h,m,s))
