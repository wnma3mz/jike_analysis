# coding: utf-8
import pandas as pd
import numpy as np
import os
import json
def get_json(fname):
    return fname.endswith('.json')


f_lst = list(filter(get_json, os.listdir()))

# f_lst.sort(key=lambda item: (int(item.split('-')[2]), int(item.split('-')[3])))
columns=['topic', 'content', 'likeCount', 'repostCount', 'commentCount', 'shareCount']

for fname in f_lst:
    if fname.split('.')[0] + '.xlsx' in os.listdir():
        continue
     
    with open(f"{fname}","r") as f:
        data = json.load(f)

    data_lst = []

    for item in data['data']:
        count_lst = ['likeCount', 'repostCount', 'commentCount', 'shareCount']
        tmp_dict = {
            'content': item['content'],
            'topic': item['topic']['content']   
        }
        for count in count_lst:
            if count in item.keys():
                num = item[count]
            else:
                num = 0
            tmp_dict[count] = num
            
        data_lst.append(tmp_dict)

    df = pd.DataFrame(data_lst, columns=columns)
    df.to_excel(f"{fname.split('.')[0]}.xlsx", encoding='utf8')