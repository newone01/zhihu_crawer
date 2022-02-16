import json
import datetime
from datebase import zhihu_cookies_db

path = 'test/cookies'

with open(path, 'r') as f:
    res = f.read()

res = eval(res)


zhihu_cookies_db.insert_one(res)