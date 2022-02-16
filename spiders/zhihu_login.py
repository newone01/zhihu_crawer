import os
import time
import requests
import cv2
# from check_cookies import CheckCookies
from CookiePool.utils.slide_crack import SlideCrack
from CookiePool.spiders.check_cookies import CheckCookies
from CookiePool.spiders.selenium_base import *
from CookiePool.logger import logger

url = 'https://www.zhihu.com/signin?next=%2F'


def download_img(url):
    headers = {
        'authority': 'necaptcha.nosdn.127.net',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    filename = url.split('/')[-1]
    # 通过将url切割从/后开始获取文件名
    req = requests.get(url, headers=headers)
    path = os.path.join('imgs', filename)
    with open(path, 'wb') as f:
        f.write(req.content)
    return path

def login(username, password):
    brower = get_brower(headless=True)
    try:
        brower.get(url)


        # 使用密码登陆
        tab = brower.find_element_css_selector(
            '#root > div > main > div > div > div > div.SignContainer-content > div > div:nth-child(1) > form > div.SignFlow-tabs > div:nth-child(2)'
        )
        tab.click()

        # 账号
        username_element = brower.find_element_css_selector(
            '#root > div > main > div > div > div > div.SignContainer-content > div > div:nth-child(1) > form > div.SignFlow-account > div > label > input'
        )
        username_element.send_keys(username)

        # 密码
        password_element = brower.find_element_css_selector(
            '#root > div > main > div > div > div > div.SignContainer-content > div > div:nth-child(1) > form > div.SignFlow-password > div > label > input'
        )
        password_element.send_keys(password)

        # 点击登陆
        submit_css = '#root > div > main > div > div > div > div.SignContainer-content > div > div:nth-child(1) > form > button'

        wait_element(brower, submit_css)
        submit = brower.find_element_css_selector(submit_css)
        time.sleep(1)
        submit.click()

        bg_url = None
        for i in range(5):
            # 滑块背景图
            bg_css = 'body > div.yidun_popup--light.yidun_popup > div.yidun_modal__wrap > div > div > div.yidun_modal__body > div > div.yidun_panel > div > div.yidun_bgimg'
            try:
                wait_element_css(brower, bg_css, 5)
            except:
                # 如果滑块没有出现则再次尝试
                submit.click()
            bg_url = brower.find_element_css_selector(bg_css).get_attribute('src')
            if bg_url:
                break
            else:
                time.sleep(0.5)
        bg_path = download_img(bg_url)

        # 滑块本身
        target_css = 'body > div.yidun_popup--light.yidun_popup > div.yidun_modal__wrap > div > div > div.yidun_modal__body > div > div.yidun_panel > div > div.yidun_bgimg > img.yidun_jigsaw'
        wait_element_css(brower, target_css)
        target_url = brower.find_element_css_selector(target_css).get_attribute('src')
        target_path = download_img(target_url)
        out_path = 'img/out.png'
        sc = SlideCrack(target_path, bg_path, out_path)
        offset_x = sc.discern()

        slider = brower.find_element_css_selector(
            'body > div.yidun_popup--light.yidun_popup > div.yidun_modal__wrap > div > div > div.yidun_modal__body > div > div.yidun_control > div.yidun_slider > span'
        )
        action = webdriver.ActionChains(brower)
        # 背景图片在浏览器中的大小
        brower_bg_width = int(brower.find_element_css_selector(bg_css).get_attribute('src'))
        # 下载图片宽度
        local_bg_width = int(cv2.imread(bg_path).shape[1])
        # 不同计算机显示器尺寸和清晰度不同需要进行计算
        ratio = float(local_bg_width / brower_bg_width)
        # 10 是实际屏幕计算的结果
        offset_x = offset_x / ratio + 10
        action.click_and_hold(slider).move_by_offset(offset_x, 0)
        time.sleep(0.5)
        action.release().perform()
        print('登陆 成功')


    except Exception as e:
        pass
        # logger.error(f'登陆失败， error: {e}')

    finally:
        time.sleep(5)
        cookies = brower.get_cookies()
        # 如果获取cookies后，没有通过check， 则再次获取，避免网络原因导致部分cookies没有加载完成
        for i in range(5):
            if CheckCookies.zhihu_check_cookies(cookies):
                break
            time.sleep(2)
            cookies = brower.get_cookies()
        all_header_info = get_brower_header(brower)
        brower.close()
    return cookies, all_header_info

cookies, all_header = login('13995976722', 'Szypzsgs20.')
print(cookies)
print(all_header)