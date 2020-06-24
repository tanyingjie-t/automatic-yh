#!/usr/bin/env python
# coding: utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
from old_user import *

# 输出时间
def job():
    address = r"C:\Users\Administrator\car_y\old_user.py"
    os.system('python {}'.format(address))
# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='1-5', hour=23, minute=25)
# 每周一至五，14时48分执行job
scheduler.start()


