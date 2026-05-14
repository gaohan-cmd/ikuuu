import os
import re

import requests

session = requests.session()
# server酱
SCKEY = os.environ.get('SCKEY')
# 直接在一个环境变量中放入整段响应文本，程序会自动解析 Set-Cookie
COOKIE_RAW = os.environ.get('IKUUU_COOKIE_RAW', '')

check_url = 'https://ikuuu.win/user/checkin'

header = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'origin': 'https://ikuuu.win',
    'referer': 'https://ikuuu.win/user/profile',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


def load_cookies_from_raw(raw_text: str) -> None:
    cookie_names = ['PHPSESSID', 'uid', 'email', 'key', 'ip', 'expire_in']
    for name in cookie_names:
        match = re.search(rf'Set-Cookie:\s*{re.escape(name)}=([^;\r\n]+)', raw_text, re.IGNORECASE)
        if match:
            session.cookies.set(name, match.group(1).strip(), domain='ikuuu.win', path='/')


load_cookies_from_raw(COOKIE_RAW)


def push_message(content: str):
    if SCKEY:
        push_url = 'https://sctapi.ftqq.com/{}.send?title=ikuu签到&desp={}'.format(SCKEY, content)
        requests.post(url=push_url, timeout=10)
        print('推送成功')


try:
    print('直接执行签到...')
    if not session.cookies.get_dict():
        raise ValueError('未从环境变量 IKUUU_COOKIE_RAW 中解析到有效 cookie')
    print('当前 cookies:', session.cookies.get_dict())
    check_resp = session.post(url=check_url, headers=header, timeout=15)
    print('签到原始返回:', check_resp.text)
    result = check_resp.json()
    print(result.get('msg', '签到接口未返回 msg'))
    content = result.get('msg', '签到结果为空')

    push_message(content)
except Exception as exc:
    content = f'签到失败：{exc}'
    print(content)
    push_message(content)
