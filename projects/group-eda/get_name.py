import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys

df = pd.read_csv("https://raw.githubusercontent.com/socathie/paperplane/master/data/most_backed.csv").iloc[:,1:]
df["creator"] = df["url"].map(lambda x: x.split("/")[2])
ids = list(df["creator"])

base = "https://www.kickstarter.com/profile/{}"

def get_name(x):
    r = requests.get(base.format(x))
    soup = BeautifulSoup(r.content, "lxml")
    try:
        y = soup.find("div", class_="profile_bio").find("h2").text.strip("\n")
    except:
        y = None
    if y is not None:
        return y
    else:
        return x

if __name__ == '__main__':
    out = open('names.txt', 'ab')
    for i in ids[:-1]:
        out.write(('"' + get_name(i) + '"'+ ", ").encode('utf-8'))
    out.write(('"' + get_name(ids[-1]) + '"'+ ", ").encode('utf-8'))
    exit()
# if __name__ == '__main__':
#     results = [get_name(i) for i in ids]
#     out = open('names.txt', 'ab')
#     out.write(results)
#     exit()
