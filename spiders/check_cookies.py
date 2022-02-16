import requests
from CookiePool.logger import logger

class CheckCookies:

    @staticmethod
    def zhihu_check_cookies(cookies):
        """请求知乎个人信息接口，判断cookies是否生效"""
        url = ''
        headers = {
            'user_agent': ''
        }
        s = requests.session()
        for cookies in cookies:
            s.cookies.set(cookie['name'], cookie['value'])


        r = s.set(url, headers=headers)
        # 个人信息接口，可以查到name,cookies依旧生效
        error = r.json().get('error')
        if error:
            message = error.get('message')
            logger.warning(f'知乎cookies检测失败， message：{message}')
            return False
        else:
            return True