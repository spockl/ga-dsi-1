import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys
import numpy as np

df = pd.read_csv("https://raw.githubusercontent.com/socathie/paperplane/master/data/most_backed.csv").iloc[:,1:]

base = "https://www.kickstarter.com{}"

def get_period(url):
    r = requests.get(base.format(url))
    soup = BeautifulSoup(r.content, "lxml")
    text = soup.find("div", class_="NS_campaigns__funding_period").text
    try:
        text = text.strip()
        text = text.replace("-", "\n").split("\n")
        text = [i.strip() for i in text if len(i) > 0]
        text = text[1:]
        text[-1] = text[-1][1:-1].split()[0]
        return text
    except:
        return ["","",""]

data = np.array([get_period(i) for i in df["url"]])
data = pd.DataFrame(data, columns=["start", "end", "days"])
data["url"] = df["url"]
data.to_csv("dates.csv")
print "done"
