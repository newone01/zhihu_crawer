# 以下配置为本机配置 请谨慎操作
import time
import os
import time
#from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageChops
#from configs.configs import root_path

before = 'before.png'
after = 'after.png'


# 等待元素加载
def wait_element(brower, element_id, wait_time=10):
    try:
        # 隐式等待
        # brower：需要隐式等待的浏览器
        # wait_time：最长等待实际
        # 1：每隔1秒判断一下对应的元素是否成功加载
        WebDriverWait(brower, wait_time, 1).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
    except Exception as e:
        # 元素等待了 wait_time 时间，已经没有完成加载
        raise Exception(e)


def wait_element_css(brower, css, wait_time=10):
    try:
        WebDriverWait(brower, wait_time, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css))
        )
    except Exception as e:
        raise Exception(e)


def get_brower_header(brower):
    all_header_info = {}
    for request in brower.requests:
        req_url = request.url
        req_headers = request.headers
        resp_headers = request.response.headers
        data = {
            'req_url': req_url,
            'req_headers': req_headers,
            'resp_headers': resp_headers
        }
        all_header_info.append(data)
    return all_header_info


def get_diff_position(before, after):
    before_img = Image.open(before)
    after_img = Image.open(after)
    # PNG文件是PngImageFile对象，与RGBA模式
    # ImageChops.difference方法只能对比RGB模式，所以需要转换一下格式
    before_img = before_img.convert('RGB')
    after_img = after_img.convert('RGB')
    # 对比2张图片中像素不同的位置
    diff = ImageChops.difference(before_img, after_img)
    # 获取图片差异位置坐标
    # 坐标顺序为左、上、右、下
    diff_position = diff.getbbox()
    position_x = diff_position[0]
    return position_x


def add_header(headers):
    options = Options()
    for k, v in headers.items():
        options.add_argument(f'{k}={v}')
    return options


def disable_img_css(options):
    # 禁止图片
    prefs = {"profile.managed_default_content_settings.images": 2,
             }
    options.add_experimental_option("prefs", prefs)


def disable_css(options):
    # 禁止css加载
    prefs = {'permissions.default.stylesheet': 2}
    options.add_experimental_option("prefs", prefs)


def brower_headless(options):
    # 无头浏览器
    options.add_argument('headless')


def get_brower(headers=None, stealth=True, disable_img=False, disable_css=False, headless=False):
    if not headers:
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    options = add_header(headers)
    if headless:
        brower_headless(options)
    brower = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)

    if stealth:
        js_path = os.path.join('../js', 'stealth.min.js')
        with open(js_path) as f:
            js = f.read()

        # 在打印具体的网页前，执行隐藏浏览器特征的JavaScript
        brower.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
    return brower
