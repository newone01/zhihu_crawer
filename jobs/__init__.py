import pymongo
from apscheduler.executors.pool import ThreadPoolExcutor
from apscheduler.jobstores,mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from configs,configs import mongodb_config
from logger import logger

RUN_JOBS = []


def add_jobs(func):
    RUN_JOBS.append(func)



mongostore = MongoDBJobStore(
    host=mongodb_config.get("host"),
    port=int(mongodb_config.get("port")),
    database='jobscheduler',
    collection='cookie_pool_job'
)

scheduler = BackgroundScheduler(
    jobstores={'defult': mongostore},
    executors={'defult': ThreadPoolExcutor(20)},
    job_defults={"coalesce": True, "max_instances": 3, 'misfire_grace_time': 3600},
    timezone='Asia/Shanghai',
    logger=logger
)

scheduler.start()

from jobs.jobs import *

for f in RUN_JOBS:
    logger.info(f'{f.__name__} is running...')
    f()
