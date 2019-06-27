# coding: utf-8
import json
import os
import re
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_kv(item):
    if 'user' in item.keys():
        if 'gender' in item['user'].keys():
            gender = item['user']['gender']
        else:
            gender = 'None'

        temp = {
            'id': item['user']['id'],
            'gender': gender,
            'screenName': item['user']['screenName'],
        }
    else:
        temp = {'id': '', 'gender': '', 'screenName': ''}
    return temp


def ids_lst(fpath, f):
    """
    提取topic和subscribersCount构成字典

    @params f: json文件名
    @params fpath: json文件所在目录
    """
    with open(os.path.join(fpath, f), 'r') as f:
        data = json.load(f)['data']
    return map(generate_kv, data)


def filter_dict(id_set, data):
    """
    去除重复的id
    @params id_set：id（不重复）
    @params data：所有id的数据，经过ids_lst函数得到的

    @return lst: 将data中的话题数据进行去重
    """
    lst = []
    for id_ in id_set:
        temp_list = list(filter(lambda x: x['id'] == id_, data))
        if temp_list[0]['id']:
            tmp_dict = {
                'id': id_,
                'gender': temp_list[0]['gender'],
                'screenName': temp_list[0]['screenName'],
            }
            lst += [tmp_dict]
    return lst


if __name__ == '__main__':
    flst = os.listdir()
    ff_lst = list(
        filter(lambda f: os.path.isdir(f) and '2019' in f and '06-20' not in f,
               flst))
    ff_lst.sort(key=lambda item: item.split('.')[0].split('-')[-1])
    ids = []
    for ff in ff_lst:
        for f in os.listdir(ff):
            if f.endswith('.json'):
                ids += ids_lst(ff, f)

    id_set = set(id_['id'] for id_ in ids)

    res_dict = filter_dict(id_set, ids)
    df = pd.DataFrame(res_dict, columns=['id', 'gender', 'screenName'])
    gender_count = df.groupby('gender')['screenName'].agg(['count'])
    plt.figure(figsize=(10, 10), dpi=100)
    gender_count.plot(kind='bar')
    plt.tight_layout()
    plt.savefig('count_gender.png')
