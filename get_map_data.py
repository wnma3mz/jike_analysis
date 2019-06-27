# coding: utf-8

import json
import os

import numpy as np
import pandas as pd
import requests

from data.city_code import PROVINCES, PROVINCES_WITH_CITIES

# 读取经纬度数据文件
with open("region.sql.txt", 'r', encoding="utf-8") as f:
    location_data = f.readlines()[15:]


def get_location2(city):
    """
    根据本地的sql文件获取经纬度
    @params city: 城市名

    @return value_str: 经纬度的字符串
    """
    for line in location_data:
        if city in line:
            line_lst = line.split(", ")
            value_str = ",".join(
                s for s in (line_lst[3][1:-2], line_lst[4][1:-2]))
            return value_str

    return ""


def get_location(city, province):
    """
    根据百度api获取经纬度
    @params city： 城市
    @params province：省份

    @return value_str: 经纬度的字符串
    """
    url = 'http://api.map.baidu.com/geocoder?address={}&output=json&key=37492c0ee6f924cb5e934fa08c6b1676&city=%E5%8C%97%E4%BA%AC%E5%B8%82'

    city_url = url.format(city)

    result = requests.get(city_url).json()["result"]

    if result:
        value_str = ",".join(
            str(value) for value in result["location"].values())
    else:
        city_url = url.format(province)
        try:
            location = requests.get(city_url).json()["result"]["location"]
            value_str = "".join(str(value) for value in location.values())
        except:
            value_str = ""
    return value_str


def get_city(province, line):
    """
    根据省份与编码获取城市与经纬度
    @params province：省份
    @params line: [id_, "country", "city", "province"]

    @return city, 经纬度字符串
    """
    for city_ in PROVINCES_WITH_CITIES[province]["cities"]:
        if line[2] in city_.keys():
            city = city_[line[2]]
            value_str = get_location2(city)
            if not value_str:
                value_str = get_location2(province)
            return city, value_str

    return "", ""


def get_data_lst(data):
    """
    初始化data_lst，将位置信息添加进列表
    @params data: json数据

    @return data_lst = 
    [
        [id_, "country", "city", "province"]
        ...
    ]
    """
    data_lst = []
    for item in data:
        id_ = item["id"]
        if "user" not in item.keys():
            data_lst.append([id_, "", "", ""])
            continue
        user = item["user"]
        tmp_lst = [id_]
        for col in col_lst:
            if col in user.keys():
                tmp_lst.append(user[col])
            else:
                tmp_lst.append('')

        data_lst.append(tmp_lst)
    return data_lst


def get_res_data(data):
    """
    获取单个json文件的经纬度数据
    @params data: json数据

    @return data_lst [
        [id_, "country", "city", "province", location]
        ...
    ]
    """
    data_lst = get_data_lst(data)

    for index, line in enumerate(data_lst):
        if line[-1] != "-1" and line[-1] != "":
            try:
                i = code_lst.index(line[-1])
                province = PROVINCES[i][-1]
            except:
                province = ""
            data_lst[index][-1] = province
        if line[2] != "-1" and line[2] != "" and province != "":
            city_, location = get_city(province, line)
            if city_:
                data_lst[index][2] = city_
            data_lst[index].append(location)

    return data_lst


def get_res_lst():
    """
    获取当前文件夹下所有json文件的发帖经纬度数据
    @return data_lst的叠加
    """
    flst = os.listdir()
    ff = list(filter(lambda f: os.path.isdir(f) and '2019' in f, flst))
    ff.sort(key=lambda item: item.split('.')[0].split('-')[-1])

    # ff = ['2019-06-19']
    all_lst = []
    for fpath in ff:

        f_lst = os.listdir(fpath)
        for f in f_lst:
            if f.endswith('.json'):
                with open(os.path.join(fpath, f), 'r') as f:
                    data = json.load(f)['data']
                all_lst += get_res_data(data)

    return all_lst


if __name__ == '__main__':
    col_lst = ["country", "city", "province"]
    code_lst = [item[0] for item in PROVINCES]

    all_lst = get_res_lst()

    count_frq = dict()
    for item in all_lst:
        if item[0] in count_frq.keys():
            count_frq[item[0]][-1] += 1
        elif item[2] != "" and item[2] != "-1" and item[3] != "":
            count_frq[item[0]] = item[1:] + [1]

    df = pd.DataFrame(
        count_frq.values(),
        columns=["country", "city", "province", "location", "count"])
    df.to_excel("map.xlsx", encoding="utf-8", index=None)
