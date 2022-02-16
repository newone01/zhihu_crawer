import os
import configparser
import json




# 配置文件，方便其他文件能正确访问本包中其他文件定位

filepath = os.path.abspath(os.path.dirname(__file__))
base_config_path = os.path.join(filepath, 'base.ini')
base_cf = configparser.ConfigParser()
base_cf.read(base_config_path)

# 项目根目录
root_path = os.path.join(filepath, '..')

dev = 'dev'  # 测试环境
prod = 'prod'  # 正式环境
local = 'local'  # 本地环境
env = base_cf['base']['env'] #
cf = configparser.ConfigParser()
config_path = os.path.join(filepath, env, 'configs.ini')
cf.read(config_path)

mongodb_config = {
    "host": cf["mongodb"]["host"],
    "port": cf["mongodb"]["port"]
}

userinfo_path = os.path.join(root_path, 'configs', 'userinfo.json')
with open(userinfo_path, 'r') as f:
    res = f.read()

userinfo = json.loads(res)