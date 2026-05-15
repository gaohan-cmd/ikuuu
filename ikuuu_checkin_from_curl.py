import os
import re

import requests

CHECK_URL = 'https://ikuuu.win/user/checkin'
DEFAULT_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
)

session = requests.Session()

# 直接把 cookie 字符串放到一个环境变量里即可。
# 支持以下环境变量名（按优先级顺序）：IKUUU_COOKIE_RAW / COOKIE_RAW / IKUUU_COOKIE
COOKIE_RAW = os.environ.get('IKUUU_COOKIE_RAW') or os.environ.get('COOKIE_RAW') or os.environ.get('IKUUU_COOKIE', '')
SCKEY = os.environ.get('SCKEY')


def extract_cookie_header(raw_text: str) -> str:
    raw_text = raw_text.strip().strip('"').strip("'")
    if not raw_text:
        return ''

    if 'cookie:' in raw_text.lower():
        match = re.search(r'(?im)^\s*cookie\s*:\s*(.+)$', raw_text)
        return match.group(1).strip() if match else ''

    return raw_text


def parse_cookie_header(cookie_header: str) -> dict[str, str]:
    cookies: dict[str, str] = {}
    for part in cookie_header.split(';'):
        item = part.strip()
        if not item or '=' not in item:
            continue
        name, value = item.split('=', 1)
        cookies[name.strip()] = value.strip()
    return cookies


def load_cookies_from_raw_request(raw_text: str) -> None:
    cookie_header = extract_cookie_header(raw_text)
    if not cookie_header:
        return

    for name, value in parse_cookie_header(cookie_header).items():
        session.cookies.set(name, value, domain='ikuuu.win', path='/')


def build_headers() -> dict[str, str]:
    return {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://ikuuu.win',
        'referer': 'https://ikuuu.win/user',
        'user-agent': DEFAULT_USER_AGENT,
        'x-requested-with': 'XMLHttpRequest',
    }


def push_message(content: str) -> None:
    if not SCKEY:
        return

    push_url = 'https://sctapi.ftqq.com/{}.send?title=ikuuu签到&desp={}'.format(SCKEY, content)
    requests.post(url=push_url, timeout=10)
    print('推送成功')


def main() -> None:
    print('读取到的 cookie 原始内容:', repr(COOKIE_RAW))
    load_cookies_from_raw_request(COOKIE_RAW)

    if not session.cookies.get_dict():
        raise ValueError('未解析到 Cookie，请确认环境变量是否已设置，或是否包含有效的 cookie 字符串')

    print('直接执行签到...')
    print('当前 cookies:', session.cookies.get_dict())

    resp = session.post(CHECK_URL, headers=build_headers(), timeout=15)
    print('签到原始返回:', resp.text)

    try:
        data = resp.json()
    except Exception as exc:
        raise RuntimeError(f'签到接口返回不是有效 JSON：{exc}') from exc

    msg = data.get('msg', '签到接口未返回 msg')
    print(msg)
    push_message(msg)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        content = f'签到失败：{exc}'
        print(content)
        push_message(content)
