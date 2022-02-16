import pymongo
from configs.configs import mongodb_config

# 无密码链接
import pymongo

mongo_client = pymongo.MongoClient(mongodb_config['host'], int(mongodb_config['port']))

# 存放知乎用户的cookies
zhihu_cookies_db = mongo_client['cookies']['zhihu']
