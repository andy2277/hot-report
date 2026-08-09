import requests
import os

PUSHPLUS_TOKEN = ""

def get_weibo_hot():
    """微博热搜（第三方中转接口，兼容海外）"""
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}
    url = "https://api.vvhan.com/api/hotlist/wbHot"
    try:
        resp = requests.get(url,headers=headers,timeout=12)
        json_data = resp.json()
        ret = []
        for item in json_data["data"][:12]:
            ret.append({"title":item["title"],"hot":item.get("hot","-")})
        return ret
    except Exception as e:
        return [{"title":"微博热榜获取失败","hot":str(e)}]

def get_zhihu_hot():
    """知乎热榜"""
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}
    url = "https://api.vvhan.com/api/hotlist/zhihuHot"
    try:
        resp = requests.get(url,headers=headers,timeout=12)
        json_data = resp.json()
        ret = []
        for item in json_data["data"][:12]:
            ret.append({"title":item["title"],"hot":item.get("hot","-")})
        return ret
    except Exception as e:
        return [{"title":"知乎热榜获取失败","hot":str(e)}]

def get_bilibili_hot():
    """B站热榜"""
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}
    url = "https://api.vvhan.com/api/hotlist/bilibiliHot"
    try:
        resp = requests.get(url,headers=headers,timeout=12)
        json_data = resp.json()
        ret = []
        for item in json_data["data"][:12]:
            ret.append({"title":item["title"],"hot":item.get("hot","-")})
        return ret
    except Exception as e:
        return [{"title":"B站热榜获取失败","hot":str(e)}]

def get_douyin_hot():
    """抖音热榜"""
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}
    url = "https://api.vvhan.com/api/hotlist/douyinHot"
    try:
        resp = requests.get(url,headers=headers,timeout=12)
        json_data = resp.json()
        ret = []
        for item in json_data["data"][:12]:
            ret.append({"title":item["title"],"hot":item.get("hot","-")})
        return ret
    except Exception as e:
        return [{"title":"抖音热榜获取失败","hot":str(e)}]


def build_hot_html(weibo,zhihu,bilibili,douyin):
    html = "<h2>🔥全网热搜每日汇总</h2><hr/>"

    html += "<h3>📣微博热搜</h3><ol>"
    for idx,i in enumerate(weibo,1):
        html += f"<li>{i['title']} ｜热度:{i['hot']}</li>"
    html += "</ol><hr/>"

    html += "<h3>💡知乎热榜</h3><ol>"
    for idx,i in enumerate(zhihu,1):
        html += f"<li>{i['title']} ｜热度:{i['hot']}</li>"
    html += "</ol><hr/>"

    html += "<h3>📺B站热榜</h3><ol>"
    for idx,i in enumerate(bilibili,1):
        html += f"<li>{i['title']} ｜热度:{i['hot']}</li>"
    html += "</ol><hr/>"

    html += "<h3>🎵抖音热榜</h3><ol>"
    for idx,i in enumerate(douyin,1):
        html += f"<li>{i['title']} ｜热度:{i['hot']}</li>"
    html += "</ol>"

    html += "<p><small>数据来源第三方公开接口，仅供个人学习阅读，接口存在可用性风险。</small></p>"
    return html

def send_wechat(html_content, token):
    payload = {
        "token": token,
        "title":"🔥每日全网热搜汇总",
        "content": html_content,
        "template":"html"
    }
    res = requests.post("https://www.pushplus.plus/send",json=payload)
    print("推送返回：",res.text)

if __name__ == "__main__":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    print("开始抓取各平台热搜……")
    wb = get_weibo_hot()
    zh = get_zhihu_hot()
    bl = get_bilibili_hot()
    dy = get_douyin_hot()

    html = build_hot_html(wb,zh,bl,dy)
    token_env = os.getenv("PUSHPLUS_TOKEN","")
    if token_env:
        send_wechat(html,token_env)
        print("热搜推送完成")
    else:
        print(html)
