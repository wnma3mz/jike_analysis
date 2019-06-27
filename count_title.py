# coding: utf-8
import json
import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np


def get_column_data(lst, col):
    """
    返回对应列的信息，['time', 'likeCount', 'repostCount', 'commentCount', 'shareCount'. 'content', 'topic']
    @params lst: 一个二维列表
    @params col: int 对应的列值

    @return list: 每个时间的Count值
    """
    return [item[col] for item in lst]


def get_title_lst(num):
    """
    @params num: 阈值，每天（24个文件）出现次数大于num次的topic被记录

    @return ff: 日期目录列表, res_lst: topic列表
    """
    flst = os.listdir()
    ff = list(
        filter(lambda f: os.path.isdir(f) and '2019' in f and '06-20' not in f,
               flst))
    ff.sort(key=lambda item: item.split('.')[0].split('-')[-1])

    print(f"共统计了{len(ff)}个日期")

    title_lst = []
    for f in ff:
        flst = os.listdir(f)
        for f_ in flst:
            if 'pics' in f_:
                dir_name = f_
                break
        fpath = os.listdir(os.path.join(f, dir_name))

        title_lst += list(map(lambda f: f.split('.')[0].split('-')[0], fpath))

    title_dict = Counter(title_lst).items()
    res_lst = list(filter(lambda item: item[1] >= num, title_dict))
    res_lst.sort(key=lambda item: item[1])
    return ff, res_lst


def plot_main(lst, label=False):
    """
    绘制柱状图图片
    @params lst: 包含横纵坐标的二维列表，第一列为横坐标，第二列为纵坐标
    """
    plt.cla()

    x_lst = get_column_data(lst, 0)
    y_lst = get_column_data(lst, 1)
    plt.bar(x_lst, y_lst)
    if label:
        for a, b in zip(x_lst, y_lst):
            plt.text(
                a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.plot()
    plt.show()


def one_time(x_lst, fpath='2019-06-19'):
    """
    绘制单个日期文件夹的数据
    @params x_lst: topic的list
    @params fpath: 日期文件夹

    @return None, 直接绘制图片
    """
    data_dict = {name: 0 for name in x_lst}
    f_lst = os.listdir(fpath)
    for f in f_lst:
        if f.endswith('.json'):
            with open(os.path.join(fpath, f), 'r') as f:
                data = json.load(f)['data']
            for item in data:
                title = item['topic']['content']
                if title in x_lst and data_dict[title] == 0:
                    data_dict[title] = item['topic']['subscribersCount']
                    print(title, data_dict[title])
                if 0 not in data_dict.values():
                    break
        if 0 not in data_dict.values():
            break
    data = [[key, value] for key, value in data_dict.items()]
    plot_main(data, label=True)


def more_time(x_lst, ff_lst):
    """
    绘制多个日期文件夹的数据，折线图。横坐标为时间，纵坐标为关注粉丝量
    @params x_lst: topic的list
    @params ff_lst: 排序好的日期文件夹列表

    @return None, 直接绘制图片
    """
    data_dict = {name: [] for name in x_lst}

    for num_count, ff in enumerate(ff_lst):
        f_lst = os.listdir(ff)
        for f in f_lst:
            if f.endswith('.json'):
                with open(os.path.join(ff, f), 'r') as f:
                    data = json.load(f)['data']
                for item in data:
                    title = item['topic']['content']
                    if title in x_lst and len(data_dict[title]) == num_count:
                        data_dict[title].append(
                            item['topic']['subscribersCount'])
    # return data_dict
    plt.cla()
    for key, value in data_dict.items():
        # if value[0] != 1000002:
        if len(value) == len(ff_lst) and value[0] < 100000:
            plt.plot(ff_lst, value, 'o-', label=key)
            for a, b in enumerate(value):
                plt.text(
                    a,
                    b + 0.05,
                    '%.0f' % b,
                    ha='center',
                    va='bottom',
                    fontsize=7)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.plot()
    plt.show()


if __name__ == '__main__':
    """
    Note:
    1. 运行环境为根目录
    2. 这里值得一提的是，topic关注量最大值为10000002
    """
    ff_lst, res_lst = get_title_lst(num=4)
    x_lst = get_column_data(res_lst, 0)
    # one_time(x_lst)
    # more_time(x_lst, ff_lst)
    # plot_main(res_lst)
