"""
Readers/Writers problem:
https://en.wikipedia.org/wiki/Readers%E2%80%93writers_problem

Additionally to that, we would like to be able to monitor the jobs:

Active:
12:00:01 - Thread1 - Reading
12:00:23 - Thread2 - Reading

Pending:
12:11:11 - Thread3 - Writing
12:11:12 - Thread4 - Reading

How does it work?

One scheduler thread. Each request is a "job" thread.
Each time a request comes, append it to the list, then WAIT.

The scheduler's job is to check the queue once in a while
and NOTIFY pending jobs that can be run.
"""
import threading
from collections import namedtuple
import time

Job = namedtuple('Job', 'start, task, exclusive, thread, blocker')

lock = threading.Lock()
running = []
pending = []

def read(task):
    checkin(task, False)

def write(task):
    checkin(task, True)
    
def checkin(task, exclusive):
    global pending
    blocker = threading.Lock()
    blocker.acquire()
    job = Job(time.asctime(), task, exclusive, threading.current_thread(), blocker)

    with lock:
        pending.append(job)
    
    blocker.acquire()
    


def schedule():
    with lock:
        # remove finished tasks
        while running and running[0].thread.is_alive() == False:
            running.pop(0)

        # if the running queue is empty, start next job
        if not running and pending:
            job = pending.pop(0)
            running.append(job)
            job.blocker.release()

        # if running jobs are not exclusive
        if running and running[0].exclusive == False:
            # add all pending non-exclusive jobs too
            while pending and pending[0].exclusive == False:
                job = pending.pop(0)
                running.append(job)
                job.blocker.release()

def jobs():
    with lock:
        print('Running:')
        for job in running:
            print(job)
        print('Pending:')
        for job in pending:
            print(job)
            
