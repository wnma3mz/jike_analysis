# coding: utf-8
import json
import os
from collections import Counter
import re
import matplotlib.pyplot as plt
import numpy as np

# 生成topic，subscribersCount的dict
generate_kv = lambda item: {
    'topic': item['topic']['content'],
    'subscribersCount': item['topic']['subscribersCount'],
}
# 得到标题的正则表达式
topic_re = re.compile(r'(.+)-.+\.png')


def get_column_data(lst, col):
    """
    返回对应列的信息
    @params lst: 一个二维列表
    @params col: int 对应的列值

    @return list: 每列的Count值
    """
    return [item[col] for item in lst]


def get_topic_lst(num):
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

    topic_lst = []
    for f in ff:
        flst = os.listdir(f)
        for f_ in flst:
            if 'pics' in f_:
                dir_name = f_
                break
        fpath = os.listdir(os.path.join(f, dir_name))
        topic_lst += map(lambda f: topic_re.findall(f)[0], fpath)

    topic_dict = Counter(topic_lst).items()
    res_lst = list(filter(lambda item: item[1] >= num, topic_dict))
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


def topic_Count(f, fpath):
    """
    提取topic和subscribersCount构成字典

    @params f: json文件名
    @params fpath: json文件所在目录
    """
    if f.endswith('.json'):
        with open(os.path.join(fpath, f), 'r') as f:
            data = json.load(f)['data']
        return map(generate_kv, data)
    return ''


def filter_dict(topic_set, data):
    """
    去除重复的topic，保留最大的subscribersCount
    @params topic_set：话题集合（不重复）
    @params data：所有话题的数据，经过topic_Count函数得到的

    @return lst: 将data中的话题数据进行去重
    """
    lst = []
    for topic in topic_set:
        temp_list = list(filter(lambda x: x['topic'] == topic, data))
        max_sub = max(temp_list, key=lambda x: x['subscribersCount'])
        tmp_dict = {
            'topic': topic,
            'subscribersCount': max_sub['subscribersCount'],
        }
        lst += [tmp_dict]
    return lst


def one_time(fpath='2019-06-19', return_=False):
    """
    绘制单个日期文件夹的数据
    @params fpath: 日期文件夹
    @params return_: 如果是给more_time函数调用，需要使用True，默认为False

    @return None, 直接绘制图片；或者data_lst
    """
    f_lst = os.listdir(fpath)

    x_lst = []
    for f in f_lst:
        map_data = topic_Count(f, fpath)
        if map_data:
            x_lst += map_data
    topic_set = set(map(lambda x: x['topic'], x_lst))
    data_lst = filter_dict(topic_set, x_lst)
    if return_:
        return data_lst
    data = [[item['topic'], item['subscribersCount']] for item in data_lst]
    plot_main(data, label=True)


def more_time(x_lst, ff_lst):
    """
    绘制多个日期文件夹的数据，折线图。横坐标为时间，纵坐标为关注粉丝量
    @params x_lst: topic的list
    @params ff_lst: 排序好的日期文件夹列表

    @return None, 直接绘制图片
    """
    data_dict = {name: [] for name in x_lst}

    for ff in ff_lst:
        data_lst = one_time(fpath=ff, return_=True)
        for item in data_lst:
            if item['topic'] not in x_lst:
                continue
            else:
                data_dict[item['topic']].append((ff, item['subscribersCount']))

    plt.cla()
    plt.figure(figsize=(10, 10), dpi=100)
    for key, value in data_dict.items():

        if len(value) > 3:
            value.sort(key=lambda item: item[0])
            x_lst = get_column_data(value, 0)
            y_lst = get_column_data(value, 1)
            if y_lst[0] < 100000:
                plt.plot(x_lst, y_lst, 'o-', label=key)
                for a, b in zip(x_lst, y_lst):
                    plt.text(
                        a,
                        b + 0.05,
                        '%.0f' % b,
                        ha='center',
                        va='bottom',
                        fontsize=7)
    plt.legend(loc=2, bbox_to_anchor=(1.05, 1.0), borderaxespad=0.)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.plot()
    # plt.savefig('count_title.png')

    plt.show()


if __name__ == '__main__':
    """
    Note:
    1. 运行环境为根目录
    2. 这里值得一提的是，topic关注量最大值为10000002
    """
    ff_lst, res_lst = get_topic_lst(num=1)
    x_lst = get_column_data(set(res_lst), 0)
    # one_time(x_lst)
    more_time(x_lst, ff_lst)
    # plot_main(res_lst)
