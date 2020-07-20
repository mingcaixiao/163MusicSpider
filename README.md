本项目使用开源项目proxy_pool提供免费代理
地址为https://github.com/jhao104/proxy_pool

## 各文件作用

**musicCommentsSpider.py**:爬取评论信息，设置了代理，不能直接运行，需要下载并且运行proxy_pool

**musicCommentsSpider_noProxies.py**:爬取评论信息，未设置代理，能够直接运行，使用过久会被封禁ip

**userInfoSpider.py**：爬取用户信息

**commentsTime.py**: 转化评论时间格式

**userInfoAnalysis.py**:处理用户信息数据并做简单分析

**commetsWordCloud.py**:生成评论词云ip