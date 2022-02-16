from jobs import scheduler, add_jobs
from jobs.refresh_cookies import RefreshCookiesJob

@add_jobs
def refresh_cookies():
    """凌晨刷新cookies"""

    # 测试，每分钟执行一次任务
    # scheduler.add_job(RefreshCookiesJob.run,
    #                   trigger='interval',
    #                   id='refresh_cookies_test',
    #                   minutes=1,
    #                   replace_existing=True)

    # 每日凌晨执行任务，minute=1避免临界情况
    scheduler.add_job(RefreshCookiesJob.run,
                      trigger='cron',
                      id='refresh_cookies',
                      hour=0,
                      minute=1,
                      second=0,
                      replace_exisiting=True)