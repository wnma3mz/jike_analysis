# coding: utf-8

import json
import multiprocessing
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

count_lst = ['likeCount', 'repostCount', 'commentCount', 'shareCount']


def f_sort_key(fname):
    """
    @params fname: 文件名 2019-06-24-00.json
    @return 天和小时，并以此排序
    """
    fname = fname.split('.')[0].split('-')
    return (int(fname[2]), int(fname[3]))


def flst_sort():
    """
    @return f_lst: 返回过滤排序后的文件列表
    """
    # 获取当前文件夹下所有以json结尾的文件
    f_lst = list(filter(lambda fname: fname.endswith('.json'), os.listdir()))
    # 根据时间排序
    f_lst.sort(key=f_sort_key)
    return f_lst


f_lst = flst_sort()


def get_ids(f_lst, num=3):
    """
    获取所有帖子的id号（去重）
    @params f_lst: 经过排序过滤的文件名
    @params num: 大于num次的id帖子才会被记录

    @return id_set: 去重且符合条件的id集合
    """
    id_lst = []
    for fname in f_lst:
        with open(f"{fname}", "r") as f:
            try:
                data = json.load(f)['data']
            except:
                continue

        id_lst += [item['id'] for item in data]

    id_set = set()
    for id_ in set(id_lst):
        if id_lst.count(id_) > num:
            id_set.add(id_)

    return id_set


def get_y_lst(item):
    """
    提取帖子中所有信息
    @params item: 一个dict，包含一个帖子的所有信息
    @return list: 由['likeCount', 'repostCount', 'commentCount', 'shareCount', 'followedCount']组成的list
    """
    y_count_lst = [
        item[count] if count in item.keys() else 0 for count in count_lst
    ]
    if 'user' in item.keys():
        return y_count_lst + [item['user']['statsCount']['followedCount']]
    else:
        return y_count_lst + [0]


def column(lst, col):
    """
    返回对应列的信息，['time', 'likeCount', 'repostCount', 'commentCount', 'shareCount'. 'content', 'topic']
    @params lst: 一个二维列表
    @params col: int 对应的列值

    @return list: 每个时间的Count值
    """
    return [item[col] for item in lst]


def id_text(f_lst, id_):
    """
    @params: f_lst: 文件列表
    @params: id_: 每个帖子的id
    
    @return content: 帖子内容
    @return topic: 话题圈名
    """
    for fname in f_lst:
        with open(f"{fname}", "r") as f:
            try:
                data = json.load(f)['data']
            except:
                continue

        for item in data:
            if item['id'] == id_:
                content = item['content'] if item['content'] else (' ')
                topic = item['topic']['content']
                return content, topic

    return '', ''


def xydata(fname, id_):
    """
    @params fname: 文件名
    @params id_: 帖子id

    时间，'likeCount', 'repostCount', 'commentCount', 'shareCount', followedCount
    @return list: 时间（横坐标）和数据（纵坐标）
    """
    with open(f"{fname}", "r") as f:
        try:
            data = json.load(f)['data']
        except:
            return []

    for item in data:
        if item['id'] == id_:
            x_time = fname.split('.')[0]
            # y_lst =
            # 时间，'likeCount', 'repostCount', 'commentCount', 'shareCount'
            return [x_time] + get_y_lst(item)

    return []


def plot_pic(data_lst, fname):
    """
    绘图
    @params data_lst: 二维list，[[1,2,3], [2,3,4]]，外层是时间，内层是数据
    @params fname: 保存的图片名
    """
    x_lst = column(data_lst, 0)
    count_lst = [
        'likeCount', 'repostCount', 'commentCount', 'shareCount',
        'user-followedCount'
    ]

    for i in range(1, 6):
        y_lst = column(data_lst, i)
        plt.plot(x_lst, y_lst, label=count_lst[i - 1])

    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.plot()

    plt.savefig(f"{fname}")


def id_dict(id_):
    id_lst = [id_ for _ in range(len(f_lst))]
    data_lst = list(
        filter(lambda item: len(item) > 0, map(xydata, f_lst, id_lst)))

    content, topic = id_text(f_lst, id_)
    d = {"id": id_, "topic": topic, "content": content, "count_data": data_lst}
    return d


# def method_1(id_set):
# return pool.map(id_dict, id_set)

# def method_2(id_set):
#     x_lst = []
#     for x in pool.imap(id_dict, id_set):
#         x_lst.append(x)
#     return x_lst

# def method_3(id_set):
#     x_lst = []
#     for x in pool.imap_unordered(id_dict, id_set):
#         x_lst.append(x)
#     return x_lst


def mk_dir():
    dir_name = time.strftime("%d-%H-%M-%S")
    os.mkdir(f"{dir_name}-txts")
    os.mkdir(f"{dir_name}-pics")
    return dir_name


if __name__ == '__main__':
    # 获取文件列表
    # Count值，用作画图
    # 时间字符串，进行归类排序
    dir_name = mk_dir()
    # 获取唯一id的集合和初始化数据字典
    id_set = get_ids(f_lst, 3)
    # id_set = list(id_set)
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)

    res = pool.map(id_dict, id_set)
    # id_data = list(map(id_dict, id_set))
    for item in res:
        # 画图前清空画布
        plt.cla()

        id_name = f"{item['topic']}-{item['id']}"
        fname = f"{dir_name}-pics/{id_name}.png"

        plot_pic(item['count_data'], fname)
        fname = f"{dir_name}-txts/{id_name}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(item['topic'] + '\n' + item['content'])
