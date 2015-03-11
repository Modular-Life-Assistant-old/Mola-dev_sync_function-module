from core import Log

from circuits import Component
import sys
import time


class Module(Component):
    __current_run = {}

    def tracefunc(self, frame, event, arg, indent=[0]):
        if frame.f_code.co_flags & 0x20:  # function is a generator
            return

        if 'call' == event:
            self.__current_run[frame] = time.time()

        elif 'return' == event:
            if time.time() - self.__current_run[frame] >= 1:
                Log.error('Function %s (%s) is not ascyn' % (
                    frame.f_code.co_name, frame.f_code.co_filename
                ))

            del(self.__current_run[frame])

        return self.tracefunc

    def started(self, c):
        sys.settrace(self.tracefunc)
