
def countdown(n):
        while n > 0:
                if n % 1000000 == 0:
                        print('> %d' % n)
                n -= 1

import time

start = time.time()

COUNT = 10 * 1000 * 1000
countdown(COUNT)

print( (time.time() - start) )

from threading import Thread

t1 = Thread(target=countdown,args=(COUNT/5,))
t2 = Thread(target=countdown,args=(COUNT/5,))
t3 = Thread(target=countdown,args=(COUNT/5,))
t4 = Thread(target=countdown,args=(COUNT/5,))
t5 = Thread(target=countdown,args=(COUNT/5,))
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()

print( (time.time() - start) )
