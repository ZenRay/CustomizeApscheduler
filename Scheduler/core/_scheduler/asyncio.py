from __future__ import absolute_import

import logging
import copy
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.asyncio import  AsyncIOExecutor

from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.redis import RedisJobStore

from apscheduler.util import undefined
from queue import PriorityQueue

# load jobstores and executors config
from Scheduler.conf import _mongodb, _redis, SCHEDULER
# load exceptions
from Scheduler.core.base.exceptions import *




class Scheduler(AsyncIOScheduler):
    """Background Scheduler

    It's Background Scheduler that customize from `apscheduler.schedulers.background`.

    Properties:
        tasks_queue: it's a priority queue that stores the tasks
        _task_name: a component of task name. Specify each job name, which 
            concatenate a unique information string, so that can store in the
            tasks_queue
        _jobstores_alias: it's a jobstores alias value that can separate each
            job. If None, set the alias value same with `_task_name`
        _executors_alias: its function is same with  _jobstores_alias, but it's 
            executors alias
    """
    def __init__(self, 
        task_name, 
        max_size=30, 
        jobstore=undefined,
        executor=undefined,
        auto_configure=True,
        **kwargs):
        """Initial Scheduler

        Arguments:
            task_name: string, a component of task name. Specify each job name, 
                which concatenate a unique information string, so that can store 
                in the tasks_queue
            max_size: int, specify the max size of the queue
            jobstore, executor:  choose a jobstore and executor. If it's 
                None, use the default scheduler configuration. Jobstore can use
                mongodb or redis, which must be choose `redis`, `mongo` or None
            
            kwargs: `BackgroundScheduler` key-word arguments
        """
        # set jobstores alias and executors alias
        
        self._task_name = task_name
        self.__max_size = max_size
        self._task_queue = PriorityQueue(maxsize=max_size)

        
        if executor in ["pool", "processpool", undefined]:
            self._executors_alias = executor
        else:
            raise NotSupportedArgument(f"Jobstore type {executor} can't be supported")

        if jobstore in ["redis", "mongo", undefined]:
            self._jobstores_alias = jobstore
        else:
            raise NotSupportedArgument(f"Jobstore type {jobstore} can't be supported")

        super().__init__(**kwargs)
        # if auto_configure is True, init the configure
        if auto_configure:
            super().configure(**SCHEDULER)
            self.add_second_jobstore()
            self.add_async_executor()


    def add_second_jobstore(self, db=14, *, jobs_key="apschedulers.second_jobs", run_times_key="apschedulers.second_run_times"):
        self._jobstores_alias = "async"
        logging.debug(f"AsyncIOScheduler add second jobstores: <{self._jobstores_alias}>")
        config = _redis.copy()
        config.update({"db": db, "jobs_key": jobs_key, "run_times_key": run_times_key})

        jobstores = RedisJobStore(**config)
        self.add_jobstore(jobstores, self._jobstores_alias)
        

    def add_async_executor(self):
        executor = AsyncIOExecutor()
        self._executors_alias = "async"
        self.add_executor(executor=executor, alias=self._executors_alias)