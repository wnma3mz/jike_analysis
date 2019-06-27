## **jike_analysis**

关于即刻热门推荐的爬虫与分析，爬取web端的[热门推荐](https://app.jike.ruguoapp.com/1.0/messages/listPopularByTag?limit=20&skip=0&tag=all)，每小时获取一次数据。对json数据进行清晰，进行二次挖掘和分析。在介绍主要工作之前，先对整个项目进行说明。

### Note

`data/`：存放的是需要查询的信息

- city_code.py: 城市编号查询，来源于[constant.py](<https://github.com/HeathLee/Schools/blob/5476612d619b5b61287e851b86ad551f2937278a/constant.py>)
- region.sql: 城市经纬度位置查询，来源于[region.sql](<https://github.com/pfinal/city/blob/1e96d38f81b491ed8a33cd63ec1e8f41cb10e1f0/region.sql>)

`2019-06-16/`：诸如此类的文件夹，为爬取到的json数据文件（由于误操作可能会有小部分数据缺失）

`spider.py`：爬虫文件，由于过于简单，故不介绍

`example/`：示例文件。`2019-06-15-23.json`：示例json文件；`2019-06-15-23.xlsx`：示例excel文件；`map.xlsx`：示例map文件；`Thermal map.png`：示例热力图

### ToExcel.py

提取每个json文件的'topic', 'content', 'likeCount', 'repostCount', 'commentCount', 'shareCount'，将其转换为excel表格

### plot_id.py

将其放入每天的json文件夹中，绘制'likeCount', 'repostCount', 'commentCount', 'shareCount', 'followedCount'随时间变化的曲线

### count_title.py

统计所有文件夹下的json文件的出现频率高的话题圈

### get_map_data.py

统计热门帖子的发帖地点，并由此得到绘制热力图数据(map.xlsx)，根据[高德平台](<https://lbs.amap.com/dev/index>)绘制热力图。

### 部分示例图

`plot_id.py`绘制的某帖图片

![example](https://raw.githubusercontent.com/wnma3mz/jike_analysis/master/2019-06-16/27-11-03-18-pics/PC玩家俱乐部-5d04496d9e840c00185c8fc4.png)

`get_map_data.py`提取的数据，根据高德开放平台绘制的热力图

![](https://raw.githubusercontent.com/wnma3mz/jike_analysis/master/example/heat_map.png)

### 写在最后

1. 如果有运行错误或者不能理解的地方欢迎提issue
2. 如果你有好的idea想要跟我分享也欢迎提issue或者直接发邮件至wnma3mz@gmail.com
3. 数据并不完全开放，如有定制需求或商业合作（包括不局限于爬虫、数据分析与挖掘、开发等），请直接发邮件wnma3mz@gmail.com

### 声明

本项目仅供交流学习

### 打赏部分

<figure class="third">
<img src="https://raw.githubusercontent.com/wnma3mz/wechat_articles_spider/master/imgs/wechat.jpg" width="260"><img src="https://raw.githubusercontent.com/wnma3mz/wechat_articles_spider/master/imgs/Alipay.jpg" width="260"><img src="https://raw.githubusercontent.com/wnma3mz/wechat_articles_spider/master/imgs/Alipay_redpaper.jpg" width="260">
</figure>