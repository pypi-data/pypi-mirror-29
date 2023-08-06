# Copyright (c) 2018, Neil Booth
#
# All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__all__ = ()

import asyncio
from collections import deque, namedtuple
from functools import partial
import inspect
import itertools
import logging
import time
import traceback


def is_async_call(func):
    '''inspect.iscoroutinefunction that looks through partials.'''
    while isinstance(func, partial):
        func = func.func
    return inspect.iscoroutinefunction(func)


# other_params: None means cannot be called with keyword arguments only
# any means any name is good
SignatureInfo = namedtuple('SignatureInfo', 'min_args max_args '
                           'required_names other_names')


def signature_info(func):
    params = inspect.signature(func).parameters
    min_args = max_args = 0
    required_names = []
    other_names = []
    no_names = False
    for p in params.values():
        if p.kind == p.POSITIONAL_OR_KEYWORD:
            max_args += 1
            if p.default is p.empty:
                min_args += 1
                required_names.append(p.name)
            else:
                other_names.append(p.name)
        elif p.kind == p.KEYWORD_ONLY:
            other_names.append(p.name)
        elif p.kind == p.VAR_POSITIONAL:
            max_args = None
        elif p.kind == p.VAR_KEYWORD:
            other_names = any
        elif p.kind == p.POSITIONAL_ONLY:
            max_args += 1
            if p.default is p.empty:
                min_args += 1
            no_names = True

    if no_names:
        other_names = None

    return SignatureInfo(min_args, max_args, required_names, other_names)


class Runner(object):

    def __init__(self):
        self.coros = deque()
        self.jobs = deque()
        self.tasks = set()
        self.cost = 0
        self.last_decay = 0


class Scheduler(object):
    '''A cost-based job scheduler.'''

    def __init__(self, loop, *, logger=None):
        self.loop = loop
        self.active = set()
        self.inactive = set()
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.event = asyncio.Event()
        self.main_task = loop.create_task(self._run_forever())
        self.running_tasks = 0
        self.timeslice = 0.05

    async def _run_forever(self):
        loop = asyncio.get_event_loop()
        while True:
            await self.event.wait()
            self._run_once()
            await asyncio.sleep(0)

    def _run_once(self):
        # Find the active runner with highest cost
        loop = self.loop
        start = loop.time()
        until = start + self.timeslice

        # Decay cost of the active runners
        for runner in self.active:
            refund = (start - runner.last_decay) / 100
            runner.cost = max(0, runner.cost - refund)
            runner.last_decay = start

        done = set()
        while loop.time() < until:
            run_list = sorted(self.active, key=lambda r:r.cost)
            if not run_list:
                self.event.clear()
                break
            runner = run_list[0]
            # Let the runner add up to 16 async jobs per event loop
            async_count = 0 if runner in done else 16
            self._run(runner, until, async_count)
            done.add(runner)

    def _run(self, runner, until, async_count):
        if runner.jobs:
            loop = self.loop
            start = loop.time()
            count = 0
            while True:
                now = loop.time()
                if now >= until or not runner.jobs:
                    break
                count += 1
                job = runner.jobs.popleft()
                try:
                    job()
                except Exception:
                    self.logger.exception('exception raised processing job')
            runner.cost += now - start
            self.logger.debug(f'ran {count} jobs in {now - start:.5f}s, '
                              f'cost now {runner.cost:.3f}')

        # Schedule up to async_count async tasks
        self._create_tasks(runner, async_count)

        # If nothing left to schedule, move to the inactive group
        if not runner.jobs and not runner.coros:
            self.active.remove(runner)
            self.inactive.add(runner)

    def _create_tasks(self, runner, count):
        count = min(count, len(runner.coros))
        if count:
            self.running_tasks += count
            runner.cost += count * 0.01   # A guess
            for n in range(count):
                coro, on_done = runner.coros.popleft()
                task = self.create_task(coro, on_done, runner)

    def _on_task_done(self, runner, on_done, task):
        runner.tasks.remove(task)
        self.running_tasks -= 1
        try:
            if on_done:
                on_done(task)
            else:
                task.result()
        except asyncio.CancelledError:
            pass
        except Exception:
            self.logger.exception('exception raised processing task result')

    def new_runner(self):
        runner = Runner()
        self.inactive.add(runner)
        return runner

    def remove_runner(self, runner):
        '''Removing a runner drop all (uncompleted) synchronous jobs.  It also
        cancels all async tasks - any already scheduled for execution
        or running in the event loop will continue to run.
        '''
        if runner in self.active:
            self.active.remove(runner)
        else:
            self.inactive.remove(runner)
        runner.jobs.clear()
        # Create tasks for all coros to avoid "coro not awaited" messages
        self._create_tasks(runner, len(runner.coros))
        # And now cancel all the runner's tasks and generate the callbacks
        for task in runner.tasks:
            task.cancel()

    def create_task(self, coro, on_done, runner):
        '''Schedule a coro to run, and call on_done when complete if not None.

        It is added to the runner's tasks so it will be cancelled if
        the runner is removed before the task completed.
        '''
        task = self.loop.create_task(coro)
        task.add_done_callback(partial(self._on_task_done, runner, on_done))
        runner.tasks.add(task)
        return task

    def add_job(self, job, runner):
        runner.jobs.append(job)
        if runner not in self.active:
            self.active.add(runner)
            self.inactive.remove(runner)
            self.event.set()

    def add_coroutine(self, coro, on_done, runner):
        runner.coros.append((coro, on_done))
        if runner not in self.active:
            self.active.add(runner)
            self.inactive.remove(runner)
            self.event.set()

    def cancel_all(self):
        '''Removes all runners (see remove_runner()) and cancels the
        main scheduling task.

        If called more than once, subsequent calls have no effect.
        '''
        runners = set.union(self.active, self.inactive)
        for runner in runners:
            self.remove_runner(runner)
        self.main_task.cancel()

    async def wait_for_all(self):
        '''Waits for all tasks to complete.'''
        tasks = set.union(set(),
                          *(runner.tasks for runner in self.active),
                          *(runner.tasks for runner in self.inactive))
        # For some reason wait requires non-empty set...
        if tasks:
            await asyncio.wait(tasks)
