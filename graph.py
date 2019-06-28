# coding: utf-8
import json
import os
import re
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np


def involvedUsers(item):
    topic = item['topic']
    content = topic['content']
    if 'involvedUsers' in topic.keys():
        users = list(
            map(lambda item: item['screenName'],
                topic['involvedUsers']['users']))
    else:
        users = ''
    string = []
    if users:
        string = [{'source': content, 'target': set(users)}]
    return string


def merge_dict(source_set, lst):
    res_lst = []
    for source in source_set:

        tmp = list(filter(lambda i: i['source'] == source, lst))
        tmp_set = set()
        for line in tmp:
            tmp_set = tmp_set | line['target']
        res_lst.append({'source': source, 'target': tmp_set})
    return res_lst


def write_data(res_lst):
    head = """
    <!DOCTYPE html>
    <meta charset="utf-8">
    <style>
        .link {
            fill: none;
            stroke: #666;
            stroke-width: 1.5px;
        }

        #licensing {
            fill: green;
        }

        .link.licensing {
            stroke: green;
        }

        .link.resolved {
            stroke-dasharray: 0, 2 1;
        }

        circle {
            fill: #ccc;
            stroke: #333;
            stroke-width: 1.5px;
        }

        text {
            font: 12px Microsoft YaHei;
            pointer-events: none;
            text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;
        }

        .linetext {
            font-size: 12px Microsoft YaHei;
        }
    </style>

    <body>
        <script src="https://d3js.org/d3.v3.min.js"></script>
        <script>
        var links = [
    """
    tail = """
    ]
       var nodes = {};

        links.forEach(function (link) {
            link.source = nodes[link.source] || (nodes[link.source] = { name: link.source });
            link.target = nodes[link.target] || (nodes[link.target] = { name: link.target });
        });

        var width = 1920, height = 1080;

        var force = d3.layout.force()
            .nodes(d3.values(nodes))
            .links(links)
            .size([width, height])
            .linkDistance(180)
            .charge(-1500)
            .on("tick", tick)
            .start();

        var svg = d3.select("body").append("svg")
            .attr("width", width)
            .attr("height", height);

        var marker =
            svg.append("marker")
                .attr("id", "resolved")
                .attr("markerUnits", "userSpaceOnUse")
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 32)
                .attr("refY", -1)
                .attr("markerWidth", 12)
                .attr("markerHeight", 12)
                .attr("orient", "auto")
                .attr("stroke-width", 2)
                .append("path")
                .attr("d", "M0,-5L10,0L0,5")
                .attr('fill', '#000000');

        var edges_line = svg.selectAll(".edgepath")
            .data(force.links())
            .enter()
            .append("path")
            .attr({
                'd': function (d) { return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y },
                'class': 'edgepath',
                'id': function (d, i) { return 'edgepath' + i; }
            })
            .style("stroke", function (d) {
                var lineColor;
                lineColor = "#B43232";
                return lineColor;
            })
            .style("pointer-events", "none")
            .style("stroke-width", 0.5)
            .attr("marker-end", "url(#resolved)");

        var edges_text = svg.append("g").selectAll(".edgelabel")
            .data(force.links())
            .enter()
            .append("text")
            .style("pointer-events", "none")
            .attr({
                'class': 'edgelabel',
                'id': function (d, i) { return 'edgepath' + i; },
                'dx': 80,
                'dy': 0
            });

        edges_text.append('textPath')
            .attr('xlink:href', function (d, i) { return '#edgepath' + i })
            .style("pointer-events", "none")
            .text(function (d) { return d.rela; });

        var circle = svg.append("g").selectAll("circle")
            .data(force.nodes())
            .enter().append("circle")
            .style("fill", function (node) {
                var color;
                var link = links[node.index];
                color = "#F9EBF9";
                return color;
            })
            .style('stroke', function (node) {
                var color;
                var link = links[node.index];
                color = "#A254A2";
                return color;
            })
            .attr("r", 28)
            .on("click", function (node) {
                edges_line.style("stroke-width", function (line) {
                    console.log(line);
                    if (line.source.name == node.name || line.target.name == node.name) {
                        return 4;
                    } else {
                        return 0.5;
                    }
                });
            })
            .call(force.drag);

        var text = svg.append("g").selectAll("text")
            .data(force.nodes())
            .enter()
            .append("text")
            .attr("dy", ".35em")
            .attr("text-anchor", "middle")
            .style('fill', function (node) {
                var color;
                var link = links[node.index];
                color = "#A254A2";
                return color;
            }).attr('x', function (d) {
                var re_en = /[a-zA-Z]+/g;
                if (d.name.match(re_en)) {
                    d3.select(this).append('tspan')
                        .attr('x', 0)
                        .attr('y', 2)
                        .text(function () { return d.name; });
                }

                else if (d.name.length <= 4) {
                    d3.select(this).append('tspan')
                        .attr('x', 0)
                        .attr('y', 2)
                        .text(function () { return d.name; });
                } else {
                    var top = d.name.substring(0, 4);
                    var bot = d.name.substring(4, d.name.length);

                    d3.select(this).text(function () { return ''; });

                    d3.select(this).append('tspan')
                        .attr('x', 0)
                        .attr('y', -7)
                        .text(function () { return top; });

                    d3.select(this).append('tspan')
                        .attr('x', 0)
                        .attr('y', 10)
                        .text(function () { return bot; });
                }
            });

        function tick() {
            circle.attr("transform", transform1);
            text.attr("transform", transform2);

            edges_line.attr('d', function (d) {
                var path = 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
                return path;
            });

            edges_text.attr('transform', function (d, i) {
                if (d.target.x < d.source.x) {
                    bbox = this.getBBox();
                    rx = bbox.x + bbox.width / 2;
                    ry = bbox.y + bbox.height / 2;
                    return 'rotate(180 ' + rx + ' ' + ry + ')';
                }
                else {
                    return 'rotate(0)';
                }
            });
        }

        function linkArc(d) {
            return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y
        }

        function transform1(d) {
            return "translate(" + d.x + "," + d.y + ")";
        }
        function transform2(d) {
            return "translate(" + (d.x) + "," + d.y + ")";
        }

    </script>
    """
    with open('example/graph.html', 'w', encoding='utf-8') as f:
        f.write(head)
        for item in res_lst:
            if len(item['target']) < 20:
                for target in item['target']:
                    f.write('{ source: "' + item['source'] + '", target: "' +
                            target + '" },' + '\n')
        f.write(tail)
    # with open('example/graph.txt', 'w', encoding='utf-8') as f:
    #     for item in res_lst:
    #         if len(item['target']) < 20:
    #             for target in item['target']:
    #                 f.write('{ source: "' + item['source'] + '", target: "' +
    #                         target + '" },' + '\n')
    # with open('example/graph.txt', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    # print(lines)


def count_user(res_data):

    target_lst = list(map(lambda item: list(item['target']), res_lst))
    target_lst = flat(target_lst)

    num = 5
    topic_dict = Counter(target_lst).items()
    target_lst = list(filter(lambda item: item[1] >= num, topic_dict))
    target_lst.sort(key=lambda item: item[1])

    lst = []
    for user in target_lst:
        tmp = {'user': user, 'topics': []}
        for item in res_lst:
            if user[0] in item['target']:
                tmp['topics'].append(item['source'])
        lst += [tmp]
    return lst


if __name__ == '__main__':
    flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]
    res_data = []

    for fpath in [
            '2019-06-16', '2019-06-17', '2019-06-18', '2019-06-19',
            '2019-06-21', '2019-06-22'
    ]:
        for f in os.listdir(fpath):
            if f.endswith('.json'):
                with open(os.path.join(fpath, f), 'r', encoding='utf-8') as f:
                    data = json.load(f)['data']
                tmp_data = list(map(involvedUsers, data))
                res_data += flat(tmp_data)

    res_data = flat(res_data)
    source_set = set(map(lambda item: item['source'], res_data))
    res_lst = merge_dict(source_set, res_data)

    # user_lst = count_user(res_lst)
    write_data(res_lst)
