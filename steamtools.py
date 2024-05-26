# -*- coding: utf-8 -*-
"""
cron: 1 0 0 * * *
new Env('SteamTools');
"""

from sendNotify import send
from curl_cffi import requests

import re
import os
import time
#requests.packages.urllib3.disable_warnings()


class SteamTools(object):
    def __init__(self,
                 cookie,
                 username,
                 login_url='https://bbs.steamtools.net/member.php',
                 checkin_url='https://bbs.steamtools.net/plugin.php?id=dc_signin:sign&inajax=1'):
        self.cookie = cookie
        self.username = username
        self.formhash = ''
        self.login_url = login_url
        self.checkin_url = checkin_url
        self.st_session = requests.Session()

    def check_cookie(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Cookie': self.cookie,
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }
        params = {
            'mod': 'viewthread',
            'tid': '8741',
        }
        try:
            rqs = self.st_session.get(
                'https://bbs.steamtools.net/forum.php', params=params, headers=headers,
                timeout=15, verify=False).text
        except Exception as e:
            print('[-] err: ', str(e))
            exit(-1)

        searchObj = re.search(
            r'<input type="hidden" name="formhash" value="(.+?)" />', rqs)

        if searchObj:
            self.formhash = searchObj.group(1)
        else:
            print('[-] cookie 不能用了')
            send("steamtools 签到结果", "steamtools Cookie已失效，请重新设置Cookie")
            print(rqs)
            exit(-1)
        print("[*] formhash: ", self.formhash)
        if username in rqs:
            print("[+] cookie能用")
        else:
            print('[-] cookie 不能用了')
            send("steamtools 签到结果", "steamtools Cookie已失效，请重新设置Cookie")
            exit(-1)

    def start(self):
        self.check_cookie()

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://bbs.steamtools.net',
            'Cookie': self.cookie,
            'priority': 'u=0, i',
            'referer': 'https://bbs.steamtools.net/forum.php?mod=viewthread&tid=8741',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        max_retries = 20
        retries = 0
        msg = ""
        while retries < max_retries:
            try:
                msg += "第{}次执行签到\n".format(str(retries+1))

                data = f'formhash={self.formhash}&signsubmit=yes&handlekey=signin&emotid=3&referer=https%3A%2F%2Fbbs.steamtools.net%2Fforum.php%3Fmod%3Dviewthread%26tid%3D8741&content=%E4%B8%BA%E4%BA%86%E7%BB%B4%E6%8A%A4%E5%AE%87%E5%AE%99%E5%92%8C%E5%B9%B3%EF%BC%8C%E6%89%93%E8%B5%B7%E7%B2%BE%E7%A5%9E%E6%9D%A5%EF%BC%81%7E%7E'

                rsp = requests.post(url=self.checkin_url, headers=headers, data=data,
                                    timeout=15, verify=False)
                rsp_text = rsp.text.strip()
                print(rsp_text)
                success = False
                if "您今日已经签过到" in rsp_text:
                    msg += '已经签到过了，不再重复签到!\n'
                    success = True
                elif "成功" in rsp_text:
                    msg += re.search(
                        r'签到成功(.*?)\'', rsp_text).group(1)
                    success = True
                else:
                    msg += "未知异常!\n"
                    msg += rsp_text + '\n'

                # rsp_json = json.loads(rsp_text)
                # print(rsp_json['code'])
                # print(rsp_json['message'])
                if success:
                    print("签到结果: ", msg)
                    send("steamtools 签到结果", msg)
                    break  # 成功执行签到，跳出循环
                elif retries >= max_retries:
                    print("达到最大重试次数，签到失败。")
                    send("steamtools 签到结果", msg)
                    break
                else:
                    retries += 1
                    print("等待20秒后进行重试...")
                    time.sleep(20)
            except Exception as e:
                print("签到失败，失败原因:"+str(e))
                send("steamtools 签到结果", str(e))
                retries += 1
                if retries >= max_retries:
                    print("达到最大重试次数，签到失败。")
                    break
                else:
                    print("等待20秒后进行重试...")
                    time.sleep(20)


if __name__ == "__main__":
    cookie = os.getenv("STEAMTOOLS_COOKIE")
    username = os.getenv("STEAMTOOLS_USER")
    SteamTools(cookie, username).start()
