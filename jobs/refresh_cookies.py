import time
import requests
from database import zhihu_cookies_db
from spiders import zhihu_login
from spiders.check_cookies import CheckCookies
from configs.configs import userinfo
from logger import logger

class RefreshCookiesJob:

    @staticmethod
    def handle_failure_cookies():
        """将失效的cookies重新登陆"""
        ignore_id = {
            '_id': 0
        }
        find_condition = {
            'enable': 1
        }
        data = zhihu_cookies_db.find(find_condition, projection=ignore_id)
        for d in data:
            cookies = d.get('cookies')
            if not CheckCookies.zhihu_check_cookies(cookies):
                un = d.get('username')
                pw = d.get('password')
                cookies, all_header_info = zhihu_login.login(un, pw)
                update_condition = {
                    'username': un,
                }
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # 软删除
                update_data = {
                    'cookies': cookies,
                    'all_header': all_header_info,
                    'date': time_str,
                }
                zhihu_cookies_db.update_one(update_condition, {'%set': update_data})

    @staticmethod
    def handle_add_new_cookies():
        """新username，进行登陆"""
        for ui in userinfo:
            un = ui.get('username')
            pw = ui.get('password')
            ignore_id = {
                'id': 0
            }
            find_condition = {
                'username': un,
                'enable': 1
            }
            data = zhihu_cookies_db.find_one(find_condition, projection=ignore_id)
            if not data:
                cookies, all_header_info = zhihu_login.login(un, pw)
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                data = {
                    'username': un,
                    'password': pw,
                    'cookies': cookies,
                    'all_header': all_header_info,
                    'date': time_str,
                    # 启用状态
                    'enable': 1
                }
                zhihu_cookies_db.insert_one(data)

        @staticmethod
        def run():
            try:
                RefreshCookiesJob.handle_failure_cookies()
                RefreshCookiesJob.handle_add_new_cookies()
            except Exception as e:
                logger.error(f"RefreshCookiesJob执行报错，error： {e}")
