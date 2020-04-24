import just
import requests
import lxml.html


ehtml = requests.get("http://unicode.org/emoji/charts-13.0/full-emoji-list.html").text


tree = lxml.html.fromstring(ehtml)

# 0 == apple
# 1 == google
nth_image = 1

base = ""
results = []
for tr in tree.xpath("//tr"):
    for th in tr.xpath(".//th"):
        if th.attrib.get("class") == "mediumhead":
            for x in th.xpath(".//a/text()"):
                base = x.replace("-", " ")
    name = ""
    uni = ""
    img_count = 0
    img = ""
    code = ""
    for td in tr.xpath(".//td"):
        td_class = td.attrib.get("class")
        if td_class == "name":
            name = td.text
        elif td_class == "chars":
            uni = td.text
        elif td_class == "code":
            code = td.xpath("./a")[0].text.replace("U+", "").replace(" ", "_")
        elif "andr" in td_class:
            if img_count == nth_image:
                imgs = td.xpath("./img/@src")
                if imgs:
                    img = imgs[0].split("base64,")[-1]
            img_count += 1

    if name and code and img:
        just.write(img, f"~/emoji_picker_images/{code}.base64", unknown_type="txt")
        results.append(f"{uni}| {name} ({base}) | {code}")

extras = [
    "😛| :P | 1F61B",
    "😀| :D | 1F600",
    "😉| ;) | 1F609",
    "😑| -_- | 1F611",
    "😜| ;P | 1F61C",
    "😕| :/ | 1F615",
    "🙁| :( | 1F641",
    "😂| lol, haha | 1F602",
    "😀| haha | 1F600",
    "😏| sneaky | 1F60F",
    "😊| blush, satisfied | 1F60A",
]

just.write("\n".join(extras + results) + "\n", "~/emojis2.txt")
