import just
import requests
import lxml.html


ehtml = requests.get("http://unicode.org/emoji/charts-13.0/full-emoji-list.html").text


tree = lxml.html.fromstring(ehtml)


base = ""
results = []
for tr in tree.xpath("//tr"):
    for th in tr.xpath(".//th"):
        if th.attrib.get("class") == "mediumhead":
            for x in th.xpath(".//a/text()"):
                base = x.replace("-", " ")
    name = ""
    uni = ""
    for td in tr.xpath(".//td"):
        td_class = td.attrib.get("class")
        if td_class == "name":
            name = td.text
        elif td_class == "chars":
            uni = td.text
    if name and uni:
        results.append(f"{uni} {name} ({base})")

extras = [
    "😛 :P",
    "😀 :D",
    "😉 ;)",
    "😑 -_-",
    "😜 ;P",
    "😕 :/",
    "🙁 :(",
    "😂 lol, haha",
    "😀 haha",
    "😏 sneaky",
    "😊 blush, satisfied",
]

just.write("\n".join(extras + results) + "\n", "~/emojis.txt")
