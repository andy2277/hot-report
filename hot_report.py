import requests
import os

PUSHPLUS_TOKEN = ""

def get_weibo_hot():
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = "https://weibo.com/ajax/side/hotSearch"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        # 判断返回是否JSON
        if resp.status_code != 200:
            raise Exception(f"HTTP状态码{resp.status_code},海外IP大概率被拦截")
        json_data = resp.json()
        ret = []
        for item in json_data["data"]["realtime"]:
            ret.append({"title": item["word"], "hot": item.get("num", 0)})
        return ret[:12]
    except Exception as e:
        return [{"title": "微博热榜获取失败（GitHub海外环境会拦截）", "hot": str(e)}]

def get_zhihu_hot():
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=12"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            raise Exception(f"HTTP状态码{resp.status_code},海外IP大概率被拦截")
        json_data = resp.json()
        ret = []
        for item in json_data["data"]:
            ret.append({"title": item["target"]["title"], "hot": item["target"]["heat"]})
        return ret
    except Exception as e:
        return [{"title": "知乎热榜获取失败（GitHub海外环境会拦截）", "hot": str(e)}]

def get_bilibili_hot():
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = "https://api.bilibili.com/x/web-interface/popular"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            raise Exception(f"HTTP状态码{resp.status_code}")
        json_data = resp.json()
        ret = []
        for item in json_data["data"]["list"][:12]:
            ret.append({"title": item["title"], "hot": item["play"]})
        return ret
    except Exception as e:
        return [{"title": "B站热榜获取失败（GitHub海外环境会拦截）", "hot": str(e)}]

def get_douyin_hot():
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            raise Exception(f"HTTP状态码{resp.status_code},海外IP大概率被拦截")
        json_data = resp.json()
        ret = []
        for item in json_data["data"]["word_list"][:12]:
            ret.append({"title": item["word"], "hot": item["hot_value"]})
        return ret
    except Exception as e:
        return [{"title": "抖音热榜获取失败（GitHub海外环境会拦截）", "hot": str(e)}]


def build_hot_html(weibo, zhihu, bilibili, douyin):
    html = "<h2>🔥全网热搜每日汇总</h2><hr/>"

    html += "<h3>📣微博热搜</h3><ol>"
    for idx, i in enumerate(weibo, 1):
        html += f"<li>{i['title']} ｜热度:{i['hot']}</li>"
    html += "</ol><hr/>"

    html += "<h3>💡知乎热榜</h3><ol>"
    for idx, i in enumerate(zhihu, 1):
        html += f"<li>{i['title']} ｜热度:{i['hot']}</li>"
    html += "</ol><hr/>"

    html += "<h3>📺B站热榜</h3><ol>"
    for idx, i in enumerate(bilibili, 1):
        html += f"<li>{i['title']} ｜播放:{i['hot']}</li>"
    html += "</ol><hr/>"

    html += "<h3>🎵抖音热榜</h3><ol>"
    for idx, i in enumerate(douyin, 1):
        html += f"<li>{i['title']} ｜热度:{i['hot']}</li>"
    html += "</ol>"

    html += "<p><small>注意：GitHub Actions为海外服务器，国内社交平台会拦截；本脚本在<strong>本机Windows（国内网络）运行可正常拿到热搜</strong>。仅供个人学习。</small></p>"
    return html

def send_wechat(html_content, token):
    payload = {
        "token": token,
        "title": "🔥每日全网热搜汇总",
        "content": html_content,
        "template": "html"
    }
    res = requests.post("https://www.pushplus.plus/send", json=payload)
    print("推送返回：", res.text)

if __name__ == "__main__":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    print("开始抓取各平台热搜……")
    wb = get_weibo_hot()
    zh = get_zhihu_hot()
    bl = get_bilibili_hot()
    dy = get_douyin_hot()

    html = build_hot_html(wb, zh, bl, dy)
    token_env = os.getenv("PUSHPLUS_TOKEN", "")
    if token_env:
        send_wechat(html, token_env)
        print("热搜推送完成")
    else:
        print(html)
