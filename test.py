import sys
print(sys.version)

import rwflow
import time
from threading import Thread
import re

flow = ''
N = 10

def appender(letter, exclusive):
    def append():
        global flow
        rwflow.checkin(letter, exclusive)
        for n in range(N):
            flow += letter
            time.sleep(0.01)
    t = Thread(target=append)
    return t    

a = appender('a', False)
b = appender('b', False)
x = appender('x', True)
c = appender('c', False)
d = appender('d', False)

for t in [a,b,x,c,d]:
    t.start()

print( rwflow.jobs() )

for t in [a,b,x,c,d]:
    t.join()

print( flow )

assert re.fullmatch('[ab]+x+[cd]+', flow)

print('-------------------------')

time.sleep(0.1)

a = appender('a', False)
b = appender('b', False)
x = appender('x', True)
c = appender('c', False)
d = appender('d', False)

for t in [a,b,x,c,d]:
    t.start()

print( rwflow.jobs() )

for t in [a,b,x,c,d]:
    t.join()

print( flow )

assert re.fullmatch('[ab]+x+[cd]+[ab]+x+[cd]+', flow)
