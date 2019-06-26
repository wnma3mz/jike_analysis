# coding: utf-8
import json
import time
from pprint import pprint

import requests

url = 'https://app.jike.ruguoapp.com/1.0/originalPosts/listTrendingPostsByShare'

url_mess = 'https://app.jike.ruguoapp.com/1.0/messages/listPopularByTag?limit=20&skip=0&tag=all'

url_topics = 'https://app.jike.ruguoapp.com/1.0/topics/recommendation/list'

payload = {
    'categoryAlias': '"RECOMMENDATION"',
}

headers = {
    'User-Agent':
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'
}

html = requests.get(url_mess, headers=headers)
data = html.json()

fname = time.strftime("%Y-%m-%d-%H")

with open(f"./{fname}.json", "w") as f:
    json.dump(data, f)
