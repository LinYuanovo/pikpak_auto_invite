import json
import hashlib
import os
import re
import time
import asyncio
import aiohttp
import uuid
import image
import recognize
from rich import print_json

DEBUG_MODE = False  # Debug模式，是否打印请求返回信息
# PROXY = input('请输入代理，如不需要直接回车:')  # 代理，如果多次出现IP问题可尝试将自己所用的魔法设置为代理。例如：使用clash则设置为 'http://127.0.0.1:7890'
PROXY = ''
PUSHPLUS_TOKEN = os.getenv('PUSHPLUS_TOKEN') or ''
INVITE_CODE = os.getenv('INVITE_CODE') or input('请输入邀请码: ')
PUSH_MSG = ''


# 检查变量
def check_env():
    invite_code_list = []
    if not PUSHPLUS_TOKEN:
        print('请按照文档设置PUSHPLUS_TOKEN环境变量')
    if not INVITE_CODE:
        print('请按照文档设置INVITE_CODE环境变量')
        raise Exception('请按照文档设置INVITE_CODE环境变量')
    else:
        if '@' in INVITE_CODE:
            invite_code_list = INVITE_CODE.split('@')
        elif '\n' in INVITE_CODE:
            invite_code_list = INVITE_CODE.split('\n')
        else:
            invite_code_list.append(INVITE_CODE)
        return invite_code_list


# 推送
async def push(content):
    if PUSHPLUS_TOKEN:
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": PUSHPLUS_TOKEN,
            "title": 'PikPak邀请通知',
            "content": content,
        }
        headers = {'Content-Type': 'application/json'}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=json.dumps(data)) as response:
                    response_data = await response.json()
                    if response_data['code'] == 200:
                        print('推送成功')
                    else:
                        print(f'推送失败，{response_data["msg"]}')
        except Exception as e:
            print(e)


# 滑块数据加密
def r(e, t):
    n = t - 1
    if n < 0:
        n = 0
    r = e[n]
    u = r["row"] // 2 + 1
    c = r["column"] // 2 + 1
    f = r["matrix"][u][c]
    l = t + 1
    if l >= len(e):
        l = t
    d = e[l]
    p = l % d["row"]
    h = l % d["column"]
    g = d["matrix"][p][h]
    y = e[t]
    m = 3 % y["row"]
    v = 7 % y["column"]
    w = y["matrix"][m][v]
    b = i(f) + o(w)
    x = i(w) - o(f)
    return [s(a(i(f), o(f))), s(a(i(g), o(g))), s(a(i(w), o(w))), s(a(b, x))]


def i(e):
    return int(e.split(",")[0])


def o(e):
    return int(e.split(",")[1])


def a(e, t):
    return str(e) + "^⁣^" + str(t)


def s(e):
    t = 0
    n = len(e)
    for r in range(n):
        t = u(31 * t + ord(e[r]))
    return t


def u(e):
    t = -2147483648
    n = 2147483647
    if e > n:
        return t + (e - n) % (n - t + 1) - 1
    if e < t:
        return n - (t - e) % (n - t + 1) + 1
    return e


def c(e, t):
    return s(e + "⁣" + str(t))


def img_jj(e, t, n):
    return {"ca": r(e, t), "f": c(n, t)}


def md5(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


async def get_sign(xid, t):
    e = [
        {"alg": "md5", "salt": "KHBJ07an7ROXDoK7Db"},
        {"alg": "md5", "salt": "G6n399rSWkl7WcQmw5rpQInurc1DkLmLJqE"},
        {"alg": "md5", "salt": "JZD1A3M4x+jBFN62hkr7VDhkkZxb9g3rWqRZqFAAb"},
        {"alg": "md5", "salt": "fQnw/AmSlbbI91Ik15gpddGgyU7U"},
        {"alg": "md5", "salt": "/Dv9JdPYSj3sHiWjouR95NTQff"},
        {"alg": "md5", "salt": "yGx2zuTjbWENZqecNI+edrQgqmZKP"},
        {"alg": "md5", "salt": "ljrbSzdHLwbqcRn"},
        {"alg": "md5", "salt": "lSHAsqCkGDGxQqqwrVu"},
        {"alg": "md5", "salt": "TsWXI81fD1"},
        {"alg": "md5", "salt": "vk7hBjawK/rOSrSWajtbMk95nfgf3"}
    ]
    md5_hash = f"YvtoWO6GNHiuCl7xundefinedmypikpak.com{xid}{t}"
    for item in e:
        md5_hash += item["salt"]
        md5_hash = md5(md5_hash)
    return md5_hash


async def get_mail():
    json_data = {
        "min_name_length": 10,
        "max_name_length": 10
    }
    url = 'https://api.internal.temp-mail.io/api/v3/email/new'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data, ssl=False) as response:
            response_data = await response.json()
            mail = response_data['email']
        return mail


# 获取邮箱的验证码内容
async def get_code(mail, max_retries=10, delay=1):
    retries = 0
    while retries < max_retries:
        url = f'https://api.internal.temp-mail.io/api/v3/email/{mail}/messages'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                html = await response.json()
                if html:
                    text = (html[0])['body_text']
                    code = re.search('\\d{6}', text).group()
                    print(f'获取邮箱验证码:{code}')
                    return code
                else:
                    time.sleep(delay)
                    retries += 1
    print("获取邮箱邮件内容失败，未收到邮件...")
    return None


async def init(xid, mail):
    url = 'https://user.mypikpak.com/v1/shield/captcha/init'
    body = {
        "client_id": "YvtoWO6GNHiuCl7x",
        "action": "POST:/v1/auth/verification",
        "device_id": xid,
        "captcha_token": "",
        "meta": {
            "email": mail
        }
    }
    headers = {
        'host': 'user.mypikpak.com',
        'content-length': str(len(json.dumps(body))),
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'referer': 'https://pc.mypikpak.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'MainWindow Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'PikPak/2.3.2.4101 Chrome/100.0.4896.160 Electron/18.3.15 Safari/537.36',
        'accept-language': 'zh-CN',
        'content-type': 'application/json',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-client-id': 'YvtoWO6GNHiuCl7x',
        'x-client-version': '2.3.2.4101',
        'x-device-id': xid,
        'x-device-model': 'electron%2F18.3.15',
        'x-device-name': 'PC-Electron',
        'x-device-sign': 'wdi10.ce6450a2dc704cd49f0be1c4eca40053xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'x-net-work-type': 'NONE',
        'x-os-version': 'Win32',
        'x-platform-version': '1',
        'x-protocol-version': '301',
        'x-provider-name': 'NONE',
        'x-sdk-version': '6.0.0'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers, ssl=False, proxy=PROXY) as response:
            response_data = await response.json()
            if 'url' in response_data:
                if DEBUG_MODE:
                    print('初始安全验证:')
                    print_json(json.dumps(response_data, indent=4))
                return response_data
            else:
                global PUSH_MSG
                PUSH_MSG += f'IP频繁，请一段时间后再试!!!\n'
                raise print('IP频繁,请更换IP或者稍后再试!!!\n', response_data['error_description'])


async def get_image(xid):
    url = "https://user.mypikpak.com/pzzl/gen"
    params = {
        "deviceid": xid,
        "traceid": ""
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, ssl=False, proxy=PROXY) as response:
            imgs_json = await response.json()
            frames = imgs_json["frames"]
            pid = imgs_json['pid']
            traceid = imgs_json['traceid']
            if DEBUG_MODE:
                print('滑块ID:')
                print_json(json.dumps(pid, indent=4))
            params = {
                'deviceid': xid,
                'pid': pid,
                'traceid': traceid
            }
            async with session.get(f"https://user.mypikpak.com/pzzl/image", params=params, ssl=False,
                                   proxy=PROXY) as response1:
                img_data = await response1.read()
                # 保存初始图片
                save_image(img_data, f'temp/1.png')
                # 保存拼图图片
                image.run(f'temp/1.png', frames)
                # 识别图片
                select_id = recognize.run()
                # 删除缓存图片
                # image.delete_img()
            json_data = img_jj(frames, int(select_id), pid)
            f = json_data['f']
            npac = json_data['ca']
            d_request_data = {
                "pid": pid,
                "device_id": xid,
                "f": f
            }
            async with session.post(f"https://paperkiteidleplus.top/document/pikpak/hash.php", json=d_request_data, ssl=False) as response1:
                response_data = await response1.json()
                d = response_data['d']
            params = {
                'pid': pid,
                'deviceid': xid,
                'traceid': traceid,
                'f': f,
                'n': npac[0],
                'p': npac[1],
                'a': npac[2],
                'c': npac[3],
                'd': d
            }
            async with session.get(f"https://user.mypikpak.com/pzzl/verify", params=params, ssl=False,
                                   proxy=PROXY) as response2:
                response_data = await response2.json()
            result = {'pid': pid, 'traceid': traceid, 'response_data': response_data}
            return result


def save_image(img_data, img_path):
    if not os.path.exists(os.path.dirname(img_path)):
        os.makedirs(os.path.dirname(img_path))
    with open(img_path, "wb") as f:
        f.write(img_data)


async def get_new_token(result, xid, captcha):
    traceid = result['traceid']
    pid = result['pid']
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://user.mypikpak.com/credit/v1/report?deviceid={xid}&captcha_token={captcha}&type"
                f"=pzzlSlider&result=0&data={pid}&traceid={traceid}", ssl=False, proxy=PROXY) as response2:
            response_data = await response2.json()
            if DEBUG_MODE:
                print('获取验证TOKEN:')
                print_json(json.dumps(response_data, indent=4))
            return response_data


async def verification(captcha_token, xid, mail):
    url = 'https://user.mypikpak.com/v1/auth/verification'
    body = {
        "email": mail,
        "target": "ANY",
        "usage": "REGISTER",
        "locale": "zh-CN",
        "client_id": "YvtoWO6GNHiuCl7x"
    }
    headers = {
        'host': 'user.mypikpak.com',
        'content-length': str(len(json.dumps(body))),
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'referer': 'https://pc.mypikpak.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'MainWindow Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'PikPak/2.3.2.4101 Chrome/100.0.4896.160 Electron/18.3.15 Safari/537.36',
        'accept-language': 'zh-CN',
        'content-type': 'application/json',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-captcha-token': captcha_token,
        'x-client-id': 'YvtoWO6GNHiuCl7x',
        'x-client-version': '2.3.2.4101',
        'x-device-id': xid,
        'x-device-model': 'electron%2F18.3.15',
        'x-device-name': 'PC-Electron',
        'x-device-sign': 'wdi10.ce6450a2dc704cd49f0be1c4eca40053xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'x-net-work-type': 'NONE',
        'x-os-version': 'Win32',
        'x-platform-version': '1',
        'x-protocol-version': '301',
        'x-provider-name': 'NONE',
        'x-sdk-version': '6.0.0'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers, ssl=False, proxy=PROXY) as response:
            response_data = await response.json()
            if DEBUG_MODE:
                print('发送验证码:')
                print_json(json.dumps(response_data, indent=4))
            return response_data


async def verify(xid, verification_id, code):
    url = 'https://user.mypikpak.com/v1/auth/verification/verify'
    body = {
        "verification_id": verification_id,
        "verification_code": code,
        "client_id": "YvtoWO6GNHiuCl7x"
    }
    headers = {
        'host': 'user.mypikpak.com',
        'content-length': str(len(json.dumps(body))),
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'referer': 'https://pc.mypikpak.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'MainWindow Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'PikPak/2.3.2.4101 Chrome/100.0.4896.160 Electron/18.3.15 Safari/537.36',
        'accept-language': 'zh-CN',
        'content-type': 'application/json',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-client-id': 'YvtoWO6GNHiuCl7x',
        'x-client-version': '2.3.2.4101',
        'x-device-id': xid,
        'x-device-model': 'electron%2F18.3.15',
        'x-device-name': 'PC-Electron',
        'x-device-sign': 'wdi10.ce6450a2dc704cd49f0be1c4eca40053xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'x-net-work-type': 'NONE',
        'x-os-version': 'Win32',
        'x-platform-version': '1',
        'x-protocol-version': '301',
        'x-provider-name': 'NONE',
        'x-sdk-version': '6.0.0'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers, ssl=False, proxy=PROXY) as response:
            response_data = await response.json()
            if DEBUG_MODE:
                print('验证码验证结果:')
                print_json(json.dumps(response_data, indent=4))
            return response_data


async def signup(xid, mail, code, verification_token):
    url = 'https://user.mypikpak.com/v1/auth/signup'
    body = {
        "email": mail,
        "verification_code": code,
        "verification_token": verification_token,
        "password": "linyuan666",
        "client_id": "YvtoWO6GNHiuCl7x"
    }
    headers = {
        'host': 'user.mypikpak.com',
        'content-length': str(len(json.dumps(body))),
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'referer': 'https://pc.mypikpak.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'MainWindow Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'PikPak/2.3.2.4101 Chrome/100.0.4896.160 Electron/18.3.15 Safari/537.36',
        'accept-language': 'zh-CN',
        'content-type': 'application/json',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-client-id': 'YvtoWO6GNHiuCl7x',
        'x-client-version': '2.3.2.4101',
        'x-device-id': xid,
        'x-device-model': 'electron%2F18.3.15',
        'x-device-name': 'PC-Electron',
        'x-device-sign': 'wdi10.ce6450a2dc704cd49f0be1c4eca40053xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'x-net-work-type': 'NONE',
        'x-os-version': 'Win32',
        'x-platform-version': '1',
        'x-protocol-version': '301',
        'x-provider-name': 'NONE',
        'x-sdk-version': '6.0.0'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers, ssl=False, proxy=PROXY) as response:
            response_data = await response.json()
            if DEBUG_MODE:
                print('注册结果:')
                print_json(json.dumps(response_data, indent=4))
            return response_data


async def init1(xid, access_token, sub, sign, t):
    url = 'https://user.mypikpak.com/v1/shield/captcha/init'
    body = {
        "client_id": "YvtoWO6GNHiuCl7x",
        "action": "POST:/vip/v1/activity/invite",
        "device_id": xid,
        "captcha_token": access_token,
        "meta": {
            "captcha_sign": "1." + sign,
            "client_version": "undefined",
            "package_name": "mypikpak.com",
            "user_id": sub,
            "timestamp": t
        },
    }
    headers = {
        'host': 'user.mypikpak.com',
        'content-length': str(len(json.dumps(body))),
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN',
        'referer': 'https://pc.mypikpak.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'MainWindow Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'PikPak/2.3.2.4101 Chrome/100.0.4896.160 Electron/18.3.15 Safari/537.36',
        'content-type': 'application/json',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-client-id': 'YvtoWO6GNHiuCl7x',
        'x-client-version': '2.3.2.4101',
        'x-device-id': xid,
        'x-device-model': 'electron%2F18.3.15',
        'x-device-name': 'PC-Electron',
        'x-device-sign': 'wdi10.ce6450a2dc704cd49f0be1c4eca40053xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'x-net-work-type': 'NONE',
        'x-os-version': 'Win32',
        'x-platform-version': '1',
        'x-protocol-version': '301',
        'x-provider-name': 'NONE',
        'x-sdk-version': '6.0.0'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers, ssl=False, proxy=PROXY) as response:
            response_data = await response.json()
            if DEBUG_MODE:
                print('二次安全验证:')
                print_json(json.dumps(response_data, indent=4))
            return response_data


async def invite(access_token, captcha_token, xid):
    url = 'https://api-drive.mypikpak.com/vip/v1/activity/invite'
    body = {
        "apk_extra": {
            "invite_code": ""
        }
    }
    headers = {
        'host': 'api-drive.mypikpak.com',
        'content-length': str(len(json.dumps(body))),
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN',
        'authorization': 'Bearer ' + access_token,
        'referer': 'https://pc.mypikpak.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) PikPak/2.3.2.4101 '
                      'Chrome/100.0.4896.160 Electron/18.3.15 Safari/537.36',
        'content-type': 'application/json',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-captcha-token': captcha_token,
        'x-client-id': 'YvtoWO6GNHiuCl7x',
        'x-client-version': '2.3.2.4101',
        'x-device-id': xid,
        'x-system-language': 'zh-CN'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers, ssl=False, proxy=PROXY) as response:
            response_data = await response.json()
            if DEBUG_MODE:
                print('获取邀请:')
                print_json(json.dumps(response_data, indent=4))
            return response_data


async def init2(xid, access_token, sub, sign, t):
    url = 'https://user.mypikpak.com/v1/shield/captcha/init'
    body = {
        "client_id": "YvtoWO6GNHiuCl7x",
        "action": "POST:/vip/v1/order/activation-code",
        "device_id": xid,
        "captcha_token": access_token,
        "meta": {
            "captcha_sign": "1." + sign,
            "client_version": "undefined",
            "package_name": "mypikpak.com",
            "user_id": sub,
            "timestamp": t
        },
    }
    headers = {
        'host': 'user.mypikpak.com',
        'content-length': str(len(json.dumps(body))),
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN',
        'referer': 'https://pc.mypikpak.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'MainWindow Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'PikPak/2.3.2.4101 Chrome/100.0.4896.160 Electron/18.3.15 Safari/537.36',
        'content-type': 'application/json',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-client-id': 'YvtoWO6GNHiuCl7x',
        'x-client-version': '2.3.2.4101',
        'x-device-id': xid,
        'x-device-model': 'electron%2F18.3.15',
        'x-device-name': 'PC-Electron',
        'x-device-sign': 'wdi10.ce6450a2dc704cd49f0be1c4eca40053xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'x-net-work-type': 'NONE',
        'x-os-version': 'Win32',
        'x-platform-version': '1',
        'x-protocol-version': '301',
        'x-provider-name': 'NONE',
        'x-sdk-version': '6.0.0'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers, ssl=False, proxy=PROXY) as response:
            response_data = await response.json()
            if DEBUG_MODE:
                print('三次安全验证:')
                print_json(json.dumps(response_data, indent=4))
            return response_data


async def activation_code(access_token, captcha, xid, in_code):
    url = 'https://api-drive.mypikpak.com/vip/v1/order/activation-code'
    body = {
        "activation_code": in_code,
        "page": "invite"
    }
    headers = {
        'host': 'api-drive.mypikpak.com',
        'content-length': str(len(json.dumps(body))),
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN',
        'authorization': 'Bearer ' + access_token,
        'referer': 'https://pc.mypikpak.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) PikPak/2.3.2.4101 '
                      'Chrome/100.0.4896.160 Electron/18.3.15 Safari/537.36',
        'content-type': 'application/json',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-captcha-token': captcha,
        'x-client-id': 'YvtoWO6GNHiuCl7x',
        'x-client-version': '2.3.2.4101',
        'x-device-id': xid,
        'x-system-language': 'zh-CN'
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=body, headers=headers, ssl=False, proxy=PROXY) as response:
                    response_data = await response.json()
                    if DEBUG_MODE:
                        print('填写邀请:')
                        print_json(json.dumps(response_data, indent=4))
                    return response_data
        except Exception as error:
            print('Error:', error)
            raise error


async def main(incode):
    global PUSH_MSG
    try:
        start_time = time.time()
        xid = str(uuid.uuid4()).replace("-", "")
        mail = await get_mail()
        Init = await init(xid, mail)
        while True:
            print('验证滑块中...')
            img_info = await get_image(xid)
            if img_info['response_data']['result'] == 'accept':
                print('验证通过!!!')
                break
            else:
                print('验证失败, 重新验证滑块中...')
        captcha_token_info = await get_new_token(img_info, xid, Init['captcha_token'])
        verification_id = await verification(captcha_token_info['captcha_token'], xid, mail)
        code = await get_code(mail)
        verification_response = await verify(xid, verification_id['verification_id'], code)
        signup_response = await signup(xid, mail, code, verification_response['verification_token'])
        current_time = str(int(time.time()))
        sign = await get_sign(xid, current_time)
        init1_response = await init1(xid, signup_response['access_token'], signup_response['sub'], sign, current_time)
        await invite(signup_response['access_token'], init1_response['captcha_token'], xid)
        init2_response = await init2(xid, signup_response['access_token'], signup_response['sub'], sign, current_time)
        activation = await activation_code(signup_response['access_token'], init2_response['captcha_token'], xid,
                                           incode)
        end_time = time.time()
        run_time = f"{(end_time - start_time):.2f}"
        if activation['add_days'] == 5:
            print(f'邀请码: {incode} ==> 邀请成功, 用时: {run_time} 秒')
            print(f'邮箱: {mail}')
            print(f'密码: linyuan666')
            PUSH_MSG += f'邀请码: {incode} ==> 邀请成功\n邮箱: {mail}\n密码: linyuan666\n'
            return
        else:
            print(f'邀请码: {incode} ==> 邀请失败, 用时: {run_time} 秒')
            PUSH_MSG += f'邀请码: {incode} ==> 邀请失败\n'
        # input('按回车键再次邀请!!!')
        await main(incode)
    except Exception as e:
        if '环境变量' in str(e):
            return
        print(f'异常捕获:{e}')
        PUSH_MSG += f'邀请异常:{e}\n'
        # print('请检查网络环境,(开启科学上网)重试!!!')
        # input('按回车键重试!!!')
        # await main()


async def run():
    global PUSH_MSG
    invite_code_list = check_env()
    for i in range(len(invite_code_list)):
        print(f'=========正在邀请第 {i + 1} 个邀请码=========')
        PUSH_MSG += f'=========第 {i + 1} 个邀请码=========\n'
        invite_code = invite_code_list[i]
        await main(invite_code)
    await push(PUSH_MSG)


asyncio.run(run())
