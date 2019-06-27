# coding: utf-8

import json
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def f_sort(fname):
    fname = fname.split('.')[0]
    return (int(fname.split('-')[2]), int(fname.split('-')[3]))


def get_f_lst():
    """
    @return f_lst: 返回过滤排序后的文件列表
    """
    f_lst = list(filter(lambda fname: fname.endswith('.json'), os.listdir()))
    # 根据时间排序
    f_lst.sort(key=f_sort)
    return f_lst


def get_ids(f_lst, num):
    """
    获取所有帖子的id号（去重）
    @params f_lst: 经过排序过滤的文件名
    @params num: 大于num次的id帖子才会被记录

    @return id_data_dict: id的字典，每个key是一个id，对应的value是二维list
            {
                'id1': {
                    'topic': 'topic1',
                    'content': 'content1',
                    'count_data': [[1,2,3,], [4,5,6]]
                },
                'id2': {
                    'topic': 'topic2',
                    'content': 'content2',
                    'count_data': [[1,2,3,], [4,5,6]]
                },
            }
    @return id_set: 去重且符合条件的id集合
    """
    id_lst = []
    for fname in f_lst:
        with open(f"{fname}", "r") as f:
            data = json.load(f)['data']

        id_lst += [item['id'] for item in data]

    id_set = set()
    for id_ in set(id_lst):
        if id_lst.count(id_) > num:
            id_set.add(id_)

    id_data_dict = {}
    for id_ in id_set:
        id_data_dict[id_] = {"topic": "", "content": "", "count_data": []}

    return id_data_dict, id_set


def get_y_lst(item):
    """
    提取帖子中所有信息
    @params item: 一个dict，包含一个帖子的所有信息
    @return list: 由['likeCount', 'repostCount', 'commentCount', 'shareCount'. 'content', 'topic']组成的list
    """
    y_count_lst = [
        item[count] if count in item.keys() else 0 for count in count_lst
    ]
    return y_count_lst


def get_column_data(lst, col):
    """
    返回对应列的信息，['time', 'likeCount', 'repostCount', 'commentCount', 'shareCount'. 'content', 'topic']
    @params lst: 一个二维列表
    @params col: int 对应的列值

    @return list: 每个时间的Count值
    """
    return [item[col] for item in lst]


def get_data_lst(fname, id_):
    """
    提取每个文件的某个id的数据
    @params fname: 文件名
    @params id_: 指定id

    @return list or None: 如果能够返回list，则文件存在此id；反之，返回[]
    @return str: 帖子内容，不存在则返回' '
    @return str: 帖子圈子，不存在则返回' '
    """
    with open(f"{fname}", "r") as f:
        data = json.load(f)['data']

    for item in data:
        if item['id'] == id_:
            x_time = fname.split('.')[0]
            y_lst = get_y_lst(item)
            content = item['content'] if item['content'] else (' ')
            topic = item['topic']['content']
            # 时间，'likeCount', 'repostCount', 'commentCount', 'shareCount', 内容, 话题
            return [x_time] + y_lst, content, topic

    return [], '', ''


def plot_pic(data_lst, fname):
    """
    绘图
    @params data_lst: 二维list，[[1,2,3], [2,3,4]]，外层是时间，内层是数据
    @params fname: 保存的图片名
    """
    x_lst = get_column_data(data_lst, 0)
    for i in range(1, 5):
        y_lst = get_column_data(data_lst, i)
        plt.plot(x_lst, y_lst, label=count_lst[i - 1])

    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.plot()

    plt.savefig(f"{fname}")


if __name__ == '__main__':
    # 获取文件列表
    f_lst = get_f_lst()
    # Count值，用作画图
    count_lst = ['likeCount', 'repostCount', 'commentCount', 'shareCount']
    # 时间字符串，进行归类排序
    dir_name = time.strftime("%d-%H-%M-%S")
    os.mkdir(f"{dir_name}-txts")
    os.mkdir(f"{dir_name}-pics")

    # 获取唯一id的集合和初始化数据字典
    id_data_dict, id_set = get_ids(f_lst, 3)

    # 遍历每个id，填充数据字典
    for id_ in id_set:
        for fname in f_lst:
            data_lst, content, topic = get_data_lst(fname, id_)
            if data_lst:
                id_data_dict[id_]['topic'] = topic
                id_data_dict[id_]['content'] = content
                id_data_dict[id_]['count_data'].append(data_lst)

    for id_ in id_set:
        # 画图前清空画布
        plt.cla()
        data = id_data_dict[id_]
        topic_name = data['topic']

        fname = f"{dir_name}-pics/{topic_name}.png"
        plot_pic(data['count_data'], fname)

        fname = f"{dir_name}-txts/{topic_name}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(data['content'])
