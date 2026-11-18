"""从 data.json 生成 feed.xml（RSS 2.0），按收录日期取最新 60 条。用法：python3 build_feed.py"""
import json, html, datetime, os
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, "data.json"), encoding="utf-8"))
CATS = {"cda":"认知CDA·识解·近化","metaphor":"批评隐喻·框架","multi":"多模态","exp":"实验·计算","lex":"一般隐喻·词汇·文学","theory":"理论·综述·书评","adj":"相邻话语研究"}
SITE = "https://sacinal.github.io/ccl_news/"
items = sorted(d["items"], key=lambda i: (i.get("added", i["date"]), i["date"], i.get("core", False)), reverse=True)[:60]
def rfc822(day):
    dt = datetime.datetime.strptime(day, "%Y-%m-%d").replace(hour=12, tzinfo=datetime.timezone.utc)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
e = html.escape
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0"><channel>',
       '<title>批评认知语言学 文献速递</title>', f'<link>{SITE}</link>',
       '<description>批评认知语言学与隐喻研究的每日文献速递</description>', '<language>zh-cn</language>',
       f'<lastBuildDate>{datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>']
for it in items:
    star = "★ " if it.get("core") else ""
    desc = f'{it.get("authors","—")} · {it["venue"]} · {CATS.get(it["cat"], it["cat"])} · {"、".join(it.get("tags", []))}'
    out.append(f'<item><title>{e(star + it["title"])}</title><link>{e(it["url"])}</link><guid isPermaLink="true">{e(it["url"])}</guid>'
               f'<pubDate>{rfc822(it.get("added", it["date"]))}</pubDate><category>{e(CATS.get(it["cat"], it["cat"]))}</category><description>{e(desc)}</description></item>')
out.append('</channel></rss>')
open(os.path.join(here, "feed.xml"), "w", encoding="utf-8").write("\n".join(out))
print("feed.xml:", len(items), "items")
