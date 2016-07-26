"""
Readers/Writers problem:
https://en.wikipedia.org/wiki/Readers%E2%80%93writers_problem

Additionally to that, we would like to be able to monitor the jobs:

Running:
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

# the lock required when processing the running or pending queues
lock = threading.Lock()

# the currently running tasks
running = []

# the currently pending tasks
pending = []

# a scheduler thread will be created as soon as a task is checked in
# and will die once all tasks are done
scheduler = None


def checkin(task, exclusive):
    blocker = threading.Lock()
    blocker.acquire()
    job = Job(time.asctime(), task, exclusive, threading.current_thread(), blocker)

    with lock:
        pending.append(job)
        
        global scheduler
        if not scheduler or not scheduler.is_alive():
            scheduler = threading.Thread(name='rwflow.scheduler', target=schedule)
            scheduler.start()
            
    blocker.acquire()
    

def schedule():
    while running or pending:
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
        
        time.sleep(0.001)
            

def jobs():
    with lock:
        print('Running:')
        for job in running:
            if job.exclusive:
                print('%s - %s (E)' % (job.start, job.task))
            else:
                print('%s - %s' % (job.start, job.task))
                
        print('\nPending:')
        for job in pending:
            if job.exclusive:
                print('%s - %s (E)' % (job.start, job.task))
            else:
                print('%s - %s' % (job.start, job.task))
            

