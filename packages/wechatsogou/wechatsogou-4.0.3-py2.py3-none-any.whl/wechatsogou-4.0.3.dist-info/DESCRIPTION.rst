基于搜狗微信搜索的微信公众号爬虫接口
====================================

|Build Status| |PyPI version| |PyPI| |py27,py35,py36| |PyPI|

.. figure:: https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_gzh_info.png
   :alt: ws\_api.get\_gzh\_info('南航青年志愿者')

   ws\_api.get\_gzh\_info('南航青年志愿者')

::

     __        __        _           _   ____
     \ \      / /__  ___| |__   __ _| |_/ ___|  ___   __ _  ___  _   _
      \ \ /\ / / _ \/ __| '_ \ / _` | __\___ \ / _ \ / _` |/ _ \| | | |
       \ V  V /  __/ (__| | | | (_| | |_ ___) | (_) | (_| | (_) | |_| |
        \_/\_/ \___|\___|_| |_|\__,_|\__|____/ \___/ \__, |\___/ \__,_|
                                                     |___/

项目简介
========

基于搜狗微信搜索的微信公众号爬虫接口，可以扩展成基于搜狗搜索的爬虫

如果有问题，请提issue

`CHANGELOG <./CHANGELOG.md>`__

交流分享
========

-  QQ群

132955136

赞助作者
========

甲鱼说，咖啡是灵魂的饮料，买点咖啡

`谢谢这些人的☕️ <./coffee.md>`__

问题集锦
========

::

    Q:没有得到原始文章url？
    A:微信屏蔽此接口，请在临时链接有效期内保存文章内容。

    Q:获取文章只能10篇？
    A:是的，仅显示最近10条群发。

    Q:使用的是python 2 还是 3？
    A:都支持，若出错，请报BUG。

安装
====

::

    pip install wechatsogou --upgrade

使用
====

初始化 API
~~~~~~~~~~

.. code:: python

    import wechatsogou

    # 可配置参数

    # 直连
    ws_api = wechatsogou.WechatSogouAPI()

    # 验证码输入错误的重试次数，默认为1
    ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)

    # 所有requests库的参数都能在这用
    # 如 配置代理，代理列表中至少需包含1个 HTTPS 协议的代理, 并确保代理可用
    ws_api = wechatsogou.WechatSogouAPI(proxies={
        "http": "127.0.0.1:8888",
        "https": "127.0.0.1:8888",
    })

    # 如 设置超时
    ws_api = wechatsogou.WechatSogouAPI(timeout=0.1)

获取特定公众号信息 - get\_gzh\_info
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_gzh_info.png
   :alt: ws\_api.get\_gzh\_info('南航青年志愿者')

   ws\_api.get\_gzh\_info('南航青年志愿者')

-  使用

   ::

       In [5]: import wechatsogou
         ...:
         ...: ws_api =wechatsogou.WechatSogouAPI()
         ...: ws_api.get_gzh_info('南航青年志愿者')
         ...:
       Out[5]:
       {
         'authentication': '南京航空航天大学',
         'headimage': 'http://img01.sogoucdn.com/app/a/100520090/oIWsFt1tmWoG6vO6BcsS7St61bRE',
         'introduction': '南航大志愿活动的领跑者,为你提供校内外的志愿资源和精彩消息.',
         'post_perm': 0,
         'profile_url': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1501140102&ver=1&signature=OpcTZp20TUdKHjSqWh7m73RWBIzwYwINpib2ZktBkLG8NyHamTvK2jtzl7mf-VdpE246zXAq18GNm*S*bq4klw==',
         'qrcode': 'http://mp.weixin.qq.com/rr?src=3&timestamp=1501140102&ver=1&signature=-DnFampQflbiOadckRJaTaDRzGSNfisIfECELSo-lN-GeEOH8-XTtM*ASdavl0xuavw-bmAEQXOa1T39*EIsjzxz30LjyBNkjmgbT6bGnZM=',
         'wechat_id': 'nanhangqinggong',
         'wechat_name': '南航青年志愿者'
       }

-  返回数据结构

   .. code:: python

       {
       'profile_url': '',  # 最近10条群发页链接
       'headimage': '',  # 头像
       'wechat_name': '',  # 名称
       'wechat_id': '',  # 微信id
       'post_perm': int,  # 最近一月群发数
       'qrcode': '',  # 二维码
       'introduction': '',  # 简介
       'authentication': ''  # 认证
       }

搜索公众号
~~~~~~~~~~

.. figure:: https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/search_gzh.png
   :alt: ws\_api.search\_gzh('南京航空航天大学')

   ws\_api.search\_gzh('南京航空航天大学')

-  使用

   ::

       In [6]: import wechatsogou
          ...:
          ...: ws_api =wechatsogou.WechatSogouAPI()
          ...: ws_api.search_gzh('南京航空航天大学')
          ...:
       Out[6]:
       [
         {
       'authentication': '南京航空航天大学',
       'headimage': 'http://img01.sogoucdn.com/app/a/100520090/oIWsFt1MvjqspMDVvZjpmxyo36sU',
       'introduction': '南京航空航天大学官方微信',
       'post_perm': 0,
       'profile_url': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1501141990&ver=1&signature=S-7U131D3eQERC8yJGVAg2edySXn*qGVi5uE8QyQU034di*2mS6vGJVnQBRB0It9t9M-Qn7ynvjRKZNQrjBMEg==',
       'qrcode': 'http://mp.weixin.qq.com/rr?src=3&timestamp=1501141990&ver=1&signature=Tlp-r0AaBRxtx3TuuyjdxmjiR4aEJY-hjh0kmtV6byVu3QIQYiMlJttJgGu0hwtZMZCCntdfaP5jD4JXipTwoGecAze8ycEF5KYZqtLSsNE=',
       'wechat_id': 'NUAA_1952',
       'wechat_name': '南京航空航天大学'
         },
         {
       'authentication': '南京航空航天大学',
       'headimage': 'http://img01.sogoucdn.com/app/a/100520090/oIWsFtwVmjdK_57vIKeMceGXF5BQ',
       'introduction': '南京航空航天大学团委官方微信平台',
       'post_perm': 0,
       'profile_url': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1501141990&ver=1&signature=aXFQrSDOiZJHedlL7vtAkvFMckxBmubE9VGrVczTwS601bOIT5Nrr8Pcgs6bQ-oEd6jdQ0aK5WCQjNwMAhJnyQ==',
       'qrcode': 'http://mp.weixin.qq.com/rr?src=3&timestamp=1501141990&ver=1&signature=7Cpbd9CVQsXJkExRcU5VM6NuyoxDQQfVfF7*CGI-PTR0y6stHPtdSDqzAzvPMWz67Xz9IMF2TDfu4Cndj5bKxlsFh6wGhiLH0b9ZKqgCW5k=',
       'wechat_id': 'nuaa_tw',
       'wechat_name': '南京航空航天大学团委'
         },
        ...
       ]

-  数据结构

list of dict, dict:

.. code:: python

    {
        'profile_url': '',  # 最近10条群发页链接
        'headimage': '',  # 头像
        'wechat_name': '',  # 名称
        'wechat_id': '',  # 微信id
        'post_perm': int,  # 最近一月群发数
        'qrcode': '',  # 二维码
        'introduction': '',  # 介绍
        'authentication': ''  # 认证
    }

搜索微信文章
~~~~~~~~~~~~

.. figure:: https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/search_article.png
   :alt: ws\_api.search\_article('南京航空航天大学')

   ws\_api.search\_article('南京航空航天大学')

-  使用

   ::

       In [7]: import wechatsogou
          ...:
          ...: ws_api =wechatsogou.WechatSogouAPI()
          ...: ws_api.search_article('南京航空航天大学')
          ...:
       Out[7]:
       [
         {
       'article': {
         'abstract': '【院校省份】江苏【报名时间】4月5日截止【考试时间】6月10日-11日南京航空航天大学2017年自主招生简章南京航空航天大学2017...',
         'imgs': ['http://img01.sogoucdn.com/net/a/04/link?appid=100520033&url=http://mmbiz.qpic.cn/mmbiz_png/P07yicBRJfC71QB3lREx4J4x34QOibGaia5BkiaaiaiaibicWkTBULou9R08K6FaxlUA1RFBFWCmpO1Lepk7ZcXK45vguQ/0?wx_fmt=png'],
         'time': 1490270644,
         'title': '南京航空航天大学2017年自主招生简章',
         'url': 'http://mp.weixin.qq.com/s?src=3&timestamp=1501142580&ver=1&signature=hRMlQOLQpu4BNhBACavusZdmk**D65qHyz5LWDq1lPjVcm7*iiBS0l7Pq40h0fiCX*bZ8vSMLzAMDNzELYFKIQ7mND0-7cQi-N0BtfTBql*CQdsHun-GtaYEqRva6Ukwce3gZh46SXJzo90kyZ3dwVYl6*589bGDIzG6JTGfpxI='
       },
       'gzh': {
         'headimage': 'http://wx.qlogo.cn/mmhead/Q3auHgzwzM5kiawibor6ABhnibMYnOADvqdcrl5XWiaFfM5mGYZ8cUica6A/0',
         'isv': 0,
         'profile_url': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1501142580&ver=1&signature=dVkDdcFr1suL1WHdCOJj7pwZhG9W*APi-j5kRtS09ccv-WID-zNs0ecDiiz1wwE7qbNSk5HBL*ffpyVXcF0fFQ==',
         'wechat_name': '自主招生在线'
       }
         },
       ...
       ]

-  数据结构

list of dict, dict:

.. code:: python

    {
        'article': {
            'title': '',  # 文章标题
            'url': '',  # 文章链接
            'imgs': '',  # 文章图片list
            'abstract': '',  # 文章摘要
            'time': int  # 文章推送时间 10位时间戳
        },
        'gzh': {
            'profile_url': '',  # 公众号最近10条群发页链接
            'headimage': '',  # 头像
            'wechat_name': '',  # 名称
            'isv': int,  # 是否加v 1 or 0
        }
    }

解析最近文章页 - get\_gzh\_article\_by\_history
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_gzh_article_by_history.png
   :alt: ws\_api.search\_article('南京航空航天大学')

   ws\_api.search\_article('南京航空航天大学')

-  使用

   ::

       In [1]: import wechatsogou
          ...:
          ...: ws_api =wechatsogou.WechatSogouAPI()
          ...: ws_api.get_gzh_article_by_history('南航青年志愿者')
          ...:
       Out[1]:
       {
         'article': [
       {
         'abstract': '我们所做的，并不能立马去改变什么——\n但千里之行，绿勤行永不止步。\n我们不会就此止步，之后我们又将再出发。\n 民勤，再见。\n绿勤行，不再见。',
         'author': '',
         'content_url': 'http://mp.weixin.qq.com/s?timestamp=1501143158&src=3&ver=1&signature=B-*tqUrFyO7OqpFeJZwTA7JJtsHpz6BgC8ugyfgpOnyWLtPb85R5Zmu0JuZRbZKG72x4bQjMCcsfA5mC3GSSOPbYd-9tzvTgmroGRmc4Tzk8090KCiEu6EjA0YMHeytWJWpxr51M2FUYQhTWJ01pTmNnXLVAG6Ex6AG52uvvmQA=',
         'copyright_stat': 100,
         'cover': 'http://mmbiz.qpic.cn/mmbiz_jpg/icFYWMxnmxHDYgXNjAle7szYLgQmicbaQlb1eVFuwp2vxEu5eNVwYacaHah2N5W8dKAm725vxv5aM6DFlM59Wftg/0?wx_fmt=jpeg',
         'datetime': 1501072594,
         'fileid': 502326199,
         'main': 1,
         'send_id': 1000000306,
         'source_url': '',
         'title': '绿勤行——不说再见',
         'type': '49'
       },
       {
         'abstract': '当时不杂，过往不恋，志愿不老，我们不散！',
         'author': '',
         'content_url': 'http://mp.weixin.qq.com/s?timestamp=1501143158&src=3&ver=1&signature=B-*tqUrFyO7OqpFeJZwTA7JJtsHpz6BgC8ugyfgpOnyWLtPb85R5Zmu0JuZRbZKG72x4bQjMCcsfA5mC3GSSOGUrM*jg*EP1jU-Dyf2CVqmPnOgBiET2wlitek4FcRbXorAswWHm*1rqODcN52NtfKD-OcRTazQS*t5SnJtu3ZA=',
         'copyright_stat': 100,
         'cover': 'http://mmbiz.qpic.cn/mmbiz_jpg/icFYWMxnmxHCoY44nPUXvkSgpZI1LaEsZfkZvtGaiaNW2icjibCp6qs93xLlr9kXMJEP3z1pmQ6TbRZNicHibGzRwh1w/0?wx_fmt=jpeg',
         'datetime': 1500979158,
         'fileid': 502326196,
         'main': 1,
         'send_id': 1000000305,
         'source_url': '',
         'title': '有始有终  |  2016-2017年度环境保护服务部工作总结',
         'type': '49'
       },
         ...
         ],
         'gzh': {
       'authentication': '南京航空航天大学',
       'headimage': 'http://wx.qlogo.cn/mmhead/Q3auHgzwzM4xV5PgPjK5XoPaaQoxnWJAFicibMvPAnsoybawMBFxua1g/0',
       'introduction': '南航大志愿活动的领跑者，为你提供校内外的志愿资源和精彩消息。',
       'wechat_id': 'nanhangqinggong',
       'wechat_name': '南航青年志愿者'
         }
       }

-  数据结构 \`\`\`python { 'gzh': { 'wechat\_name': '', # 名称
   'wechat\_id': '', # 微信id 'introduction': '', # 简介
   'authentication': '', # 认证 'headimage': '' # 头像 }, 'article': [ {
   'send\_id': int, #
   群发id，注意不唯一，因为同一次群发多个消息，而群发id一致 'datetime':
   int, # 群发datatime 10位时间戳 'type': '', #
   消息类型，均是49（在手机端历史消息页有其他类型，网页端最近10条消息页只有49），表示图文
   'main': int, # 是否是一次群发的第一次消息 1 or 0 'title': '', #
   文章标题 'abstract': '', # 摘要 'fileid': int, # 'content\_url': '',
   # 文章链接 'source\_url': '', # 阅读原文的链接 'cover': '', # 封面图
   'author': '', # 作者 'copyright\_stat': int, # 文章类型，例如：原创啊
   }, ...] }

::


    ### 解析 首页热门 页 - get_gzh_article_by_hot

    ![ws_api.get_gzh_article_by_hot(WechatSogouConst.hot_index.food)](https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_gzh_article_by_hot.png)

    - 使用

In [1]: from pprint import pprint ...: from wechatsogou import
WechatSogouAPI, WechatSogouConst ...: ...: ws\_api = WechatSogouAPI()
...: gzh\_articles =
ws\_api.get\_gzh\_article\_by\_hot(WechatSogouConst.hot\_index.food)
...: for i in gzh\_articles: ...: pprint(i) ...: { 'article': {
'abstract':
'闷热的夏天有什么事情能比吃上凉凉的甜品更惬意的呢？快一起动手做起来吧，简单方便，放冰箱冻一冻，那感觉~橙汁蒸木瓜木瓜1个（300-400克左右），橙子4个，枫糖浆20克（如果家里没有，也可以用蜂蜜、炼乳等代替），椰果适量。做法1．用削皮',
'main\_img':
'http://img01.sogoucdn.com/net/a/04/link?appid=100520033&url=http%3A%2F%2Fmmbiz.qpic.cn%2Fmmbiz\_jpg%2Fw9UGwFPia7QTUIadPibgW8OFkqf1ibR40xicKfzofRS0sDpaFp3CG0jkPyQKeXl44TXswztW1SJnic7tmCibjB8rIIGw%2F0%3Fwx\_fmt%3Djpeg',
'open\_id': 'oIWsFty9hHVI9F10amtzx5TOWIq8', 'time': 1501325220, 'title':
'夏日甜品制作方法，不收藏后悔哦!', 'url':
'http://mp.weixin.qq.com/s?src=3&timestamp=1501328525&ver=1&signature=n9*oX0k4YbNFhNMsOjIekYrsha44lfBSCbG9jicAbGYrWNN8*\ 48NzpcaHdxwUnC12syY5-ZxwcBfiJlMzdbAwWKlo26EW14w2Ax\ *gjLVlOX-AGXB4443obZ-GK0pw*\ AFZAGZD8sI4AFBZSZpyeaxN4sS7cpynxdIuw6S2h\*--LI='
}, 'gzh': { 'headimage':
'http://img03.sogoucdn.com/app/a/100520090/oIWsFty9hHVI9F10amtzx5TOWIq8',
'wechat\_name': '甜品烘焙制作坊' } } ... ... \`\`\`

-  数据结构

   .. code:: python

       {
       'gzh': {
           'headimage': str,  # 公众号头像
           'wechat_name': str,  # 公众号名称
       },
       'article': {
           'url': str,  # 文章临时链接
           'title': str,  # 文章标题
           'abstract': str,  # 文章摘要
           'time': int,  # 推送时间，10位时间戳
           'open_id': str,  # open id
           'main_img': str  # 封面图片
       }
       }

获取关键字联想词
~~~~~~~~~~~~~~~~

-  使用

   ::

       In [1]: import wechatsogou
          ...:
          ...: ws_api =wechatsogou.WechatSogouAPI()
          ...: ws_api.get_sugg('高考')
          ...:
       Out[1]:
       ['高考e通',
        '高考专业培训',
        '高考地理俱乐部',
        '高考志愿填报咨讯',
        '高考报考资讯',
        '高考教育',
        '高考早知道',
        '高考服务志愿者',
        '高考机构',
        '高考福音']

-  数据结构

关键词列表

.. code:: python

    ['a', 'b', ...]

--------------

TODO
====

-  [x] [STRIKEOUT:相似文章的公众号获取]
-  [ ] 主页热门公众号获取
-  [ ] 文章详情页信息
-  [x] [STRIKEOUT:所有类型的解析]
-  [ ] 验证码识别
-  [ ] 接入爬虫框架
-  [x] 兼容py2

--------------

.. |Build Status| image:: https://travis-ci.org/Chyroc/WechatSogou.svg?branch=master
   :target: https://github.com/Chyroc/WechatSogou
.. |PyPI version| image:: https://badge.fury.io/py/wechatsogou.svg
   :target: https://github.com/Chyroc/WechatSogou
.. |PyPI| image:: https://img.shields.io/pypi/wheel/wechatsogou.svg
   :target: https://github.com/Chyroc/WechatSogou
.. |py27,py35,py36| image:: https://img.shields.io/pypi/pyversions/wechatsogou.svg
   :target: https://github.com/Chyroc/WechatSogou
.. |PyPI| image:: https://img.shields.io/pypi/l/wechatsogou.svg
   :target: https://github.com/Chyroc/WechatSogou


Change Log
==========

`v4.0.1 <https://github.com/Chyroc/WechatSogou/tree/v4.0.1>`__ (2017-10-16)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/Chyroc/WechatSogou/compare/v4.0.0...v4.0.1>`__

**Closed issues:**

-  ws\_api.get\_gzh\_article\_by\_history(keywords)接口返回Index Error
   `#152 <https://github.com/Chyroc/WechatSogou/issues/152>`__

**Merged pull requests:**

-  Fix lxml no data
   `#153 <https://github.com/Chyroc/WechatSogou/pull/153>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Release/v4.0.0
   `#151 <https://github.com/Chyroc/WechatSogou/pull/151>`__
   (`Chyroc <https://github.com/Chyroc>`__)

`v4.0.0 <https://github.com/Chyroc/WechatSogou/tree/v4.0.0>`__ (2017-10-12)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/Chyroc/WechatSogou/compare/v3.1.2...v4.0.0>`__

**Closed issues:**

-  get\_gzh\_artilce\_by\_history 名字修改
   `#149 <https://github.com/Chyroc/WechatSogou/issues/149>`__
-  按照示例跑出来是乱码
   `#148 <https://github.com/Chyroc/WechatSogou/issues/148>`__
-  请问在阿里云ECS上出现需要输入验证码的时候该怎么解决？
   `#146 <https://github.com/Chyroc/WechatSogou/issues/146>`__
-  get\_gzh\_artilce\_by\_history 出现填写code
   `#144 <https://github.com/Chyroc/WechatSogou/issues/144>`__
-  验证码识别预估什么时候完成啊
   `#131 <https://github.com/Chyroc/WechatSogou/issues/131>`__
-  脚本定期检查python版本更新
   `#128 <https://github.com/Chyroc/WechatSogou/issues/128>`__

**Merged pull requests:**

-  fix typo artilce to article fix
   https://github.com/Chyroc/WechatSogou…
   `#150 <https://github.com/Chyroc/WechatSogou/pull/150>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  remove is\_need\_unlock
   `#147 <https://github.com/Chyroc/WechatSogou/pull/147>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Release/v3.1.2
   `#143 <https://github.com/Chyroc/WechatSogou/pull/143>`__
   (`Chyroc <https://github.com/Chyroc>`__)

`v3.1.2 <https://github.com/Chyroc/WechatSogou/tree/v3.1.2>`__ (2017-09-06)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/Chyroc/WechatSogou/compare/v3.1.1...v3.1.2>`__

**Closed issues:**

-  有代理ip更换的参数吗
   `#141 <https://github.com/Chyroc/WechatSogou/issues/141>`__
-  字符 logo 怎么生成的..
   `#140 <https://github.com/Chyroc/WechatSogou/issues/140>`__
-  求教 验证码回掉咋用 有没有示例
   `#137 <https://github.com/Chyroc/WechatSogou/issues/137>`__
-  测试的时候识别结果存储起来做分析
   `#123 <https://github.com/Chyroc/WechatSogou/issues/123>`__

**Merged pull requests:**

-  Adding an optional proxy list for api requests
   `#142 <https://github.com/Chyroc/WechatSogou/pull/142>`__
   (`jeremylinlin <https://github.com/jeremylinlin>`__)
-  Release/v3.1.1
   `#139 <https://github.com/Chyroc/WechatSogou/pull/139>`__
   (`Chyroc <https://github.com/Chyroc>`__)

`v3.1.1 <https://github.com/Chyroc/WechatSogou/tree/v3.1.1>`__ (2017-08-15)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/Chyroc/WechatSogou/compare/v3.1.0...v3.1.1>`__

**Fixed bugs:**

-  命令行和pycharm文件测试文件路径不一致的问题
   `#121 <https://github.com/Chyroc/WechatSogou/issues/121>`__

**Closed issues:**

-  作者有代理的api没有呀
   `#136 <https://github.com/Chyroc/WechatSogou/issues/136>`__
-  search\_article时只能获取到第10页，超过了获取到的就是空了
   `#132 <https://github.com/Chyroc/WechatSogou/issues/132>`__

**Merged pull requests:**

-  返回open id `#138 <https://github.com/Chyroc/WechatSogou/pull/138>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add slack invite channel link
   `#135 <https://github.com/Chyroc/WechatSogou/pull/135>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  fix test file not equal in shell vs ide (fixes 121)
   `#130 <https://github.com/Chyroc/WechatSogou/pull/130>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  search articles from wap
   `#129 <https://github.com/Chyroc/WechatSogou/pull/129>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  use hand input to unlock if not in ci env
   `#114 <https://github.com/Chyroc/WechatSogou/pull/114>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  fix docs `#113 <https://github.com/Chyroc/WechatSogou/pull/113>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Change/refactor unlock captcha
   `#112 <https://github.com/Chyroc/WechatSogou/pull/112>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add readthedocs docs
   `#111 <https://github.com/Chyroc/WechatSogou/pull/111>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Release/v3.1.0
   `#110 <https://github.com/Chyroc/WechatSogou/pull/110>`__
   (`Chyroc <https://github.com/Chyroc>`__)

`v3.1.0 <https://github.com/Chyroc/WechatSogou/tree/v3.1.0>`__ (2017-07-29)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/Chyroc/WechatSogou/compare/v3.0.0...v3.1.0>`__

**Closed issues:**

-  请教下 如何能获取到 关键词搜索 一天内的列表?
   `#73 <https://github.com/Chyroc/WechatSogou/issues/73>`__

**Merged pull requests:**

-  Add/get hot api / gzh => gzh\_info
   `#109 <https://github.com/Chyroc/WechatSogou/pull/109>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Change/search article type const
   `#108 <https://github.com/Chyroc/WechatSogou/pull/108>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Add const class and add gen hot url
   `#107 <https://github.com/Chyroc/WechatSogou/pull/107>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Add retry for captcha break
   `#106 <https://github.com/Chyroc/WechatSogou/pull/106>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  test api in real network env
   `#104 <https://github.com/Chyroc/WechatSogou/pull/104>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Release/v3.0.0
   `#103 <https://github.com/Chyroc/WechatSogou/pull/103>`__
   (`Chyroc <https://github.com/Chyroc>`__)

`v3.0.0 <https://github.com/Chyroc/WechatSogou/tree/v3.0.0>`__ (2017-07-27)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/Chyroc/WechatSogou/compare/v2.0.5...v3.0.0>`__

**Closed issues:**

-  解封成功，正在为您跳转来源地址...
   `#72 <https://github.com/Chyroc/WechatSogou/issues/72>`__
-  列表页验证码有办法绕过吗？
   `#71 <https://github.com/Chyroc/WechatSogou/issues/71>`__
-  无法正确解析wechatid
   `#70 <https://github.com/Chyroc/WechatSogou/issues/70>`__
-  貌似抓不到点赞数和阅读数
   `#65 <https://github.com/Chyroc/WechatSogou/issues/65>`__
-  badge issue `#64 <https://github.com/Chyroc/WechatSogou/issues/64>`__
-  目前getcomment接口已报错，显示 404了，何解？
   `#63 <https://github.com/Chyroc/WechatSogou/issues/63>`__
-  调用方法search\_gzh\_info()搜索公众号时，获取到的结果中wechatid为‘’
   `#62 <https://github.com/Chyroc/WechatSogou/issues/62>`__
-  跳出来验证码之后输入，报错
   `#61 <https://github.com/Chyroc/WechatSogou/issues/61>`__
-  请问logging.config.fileConfig('logging.conf')出错如何解决
   `#60 <https://github.com/Chyroc/WechatSogou/issues/60>`__
-  可否增加验证码输入错误，能再次重新输入的机制
   `#54 <https://github.com/Chyroc/WechatSogou/issues/54>`__
-  调用get\_gzh\_message返回{"ret":0,"errmsg":""}
   `#52 <https://github.com/Chyroc/WechatSogou/issues/52>`__
-  输入验证码后报错
   `#32 <https://github.com/Chyroc/WechatSogou/issues/32>`__
-  作者：对于本项目的类及方法命名，有什么建议？
   `#30 <https://github.com/Chyroc/WechatSogou/issues/30>`__
-  文章列表页也可能出现验证码
   `#29 <https://github.com/Chyroc/WechatSogou/issues/29>`__
-  功能与意见反馈，报bug可以另开issue
   `#28 <https://github.com/Chyroc/WechatSogou/issues/28>`__
-  调试几次后，开始无法爬取，是因为搜狗的反爬虫策略吗？
   `#26 <https://github.com/Chyroc/WechatSogou/issues/26>`__
-  对时间的支持
   `#19 <https://github.com/Chyroc/WechatSogou/issues/19>`__

**Merged pull requests:**

-  add get sugg
   `#102 <https://github.com/Chyroc/WechatSogou/pull/102>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Fix readme `#101 <https://github.com/Chyroc/WechatSogou/pull/101>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  modify the readme file
   `#100 <https://github.com/Chyroc/WechatSogou/pull/100>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add doc for refactored api
   `#99 <https://github.com/Chyroc/WechatSogou/pull/99>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  refactor get info from history
   `#98 <https://github.com/Chyroc/WechatSogou/pull/98>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  remove unused file / fix name / add comment
   `#97 <https://github.com/Chyroc/WechatSogou/pull/97>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  merge 原来的api 和 重构后的api
   `#96 <https://github.com/Chyroc/WechatSogou/pull/96>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Add get gzh and article by history
   `#95 <https://github.com/Chyroc/WechatSogou/pull/95>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Add get gzh by id or name
   `#94 <https://github.com/Chyroc/WechatSogou/pull/94>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add search article api
   `#93 <https://github.com/Chyroc/WechatSogou/pull/93>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add callback func
   `#92 <https://github.com/Chyroc/WechatSogou/pull/92>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  split test / add error html
   `#91 <https://github.com/Chyroc/WechatSogou/pull/91>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Add annotation and remove all type from history page
   `#89 <https://github.com/Chyroc/WechatSogou/pull/89>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Add annotation and fix
   `#88 <https://github.com/Chyroc/WechatSogou/pull/88>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  split test get gzh\_info and articel
   `#87 <https://github.com/Chyroc/WechatSogou/pull/87>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add structuring-gzh-article-from-history
   `#86 <https://github.com/Chyroc/WechatSogou/pull/86>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Structuring gzh from history
   `#85 <https://github.com/Chyroc/WechatSogou/pull/85>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  test struct article list
   `#84 <https://github.com/Chyroc/WechatSogou/pull/84>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Structuring gzh by search
   `#83 <https://github.com/Chyroc/WechatSogou/pull/83>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  fix repo language
   `#82 <https://github.com/Chyroc/WechatSogou/pull/82>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  fix repo language
   `#81 <https://github.com/Chyroc/WechatSogou/pull/81>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Search gzh article text
   `#80 <https://github.com/Chyroc/WechatSogou/pull/80>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add test gen search gzh url
   `#79 <https://github.com/Chyroc/WechatSogou/pull/79>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Refactor gen search url
   `#78 <https://github.com/Chyroc/WechatSogou/pull/78>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  release v2.0.4 -> v2.0.5
   `#77 <https://github.com/Chyroc/WechatSogou/pull/77>`__
   (`Chyroc <https://github.com/Chyroc>`__)

`v2.0.5 <https://github.com/Chyroc/WechatSogou/tree/v2.0.5>`__ (2017-07-22)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/Chyroc/WechatSogou/compare/v2.0.4...v2.0.5>`__

**Merged pull requests:**

-  fix setup python version name
   `#76 <https://github.com/Chyroc/WechatSogou/pull/76>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Release/v2.0.4
   `#75 <https://github.com/Chyroc/WechatSogou/pull/75>`__
   (`Chyroc <https://github.com/Chyroc>`__)

`v2.0.4 <https://github.com/Chyroc/WechatSogou/tree/v2.0.4>`__ (2017-07-22)
---------------------------------------------------------------------------

`Full
Changelog <https://github.com/Chyroc/WechatSogou/compare/v2.0.3...v2.0.4>`__

**Closed issues:**

-  pip 安装 No module named requests 什么情况
   `#59 <https://github.com/Chyroc/WechatSogou/issues/59>`__
-  微信搜索公众号结果模版改变了
   `#51 <https://github.com/Chyroc/WechatSogou/issues/51>`__
-  ImportError: cannot import name config
   `#40 <https://github.com/Chyroc/WechatSogou/issues/40>`__

**Merged pull requests:**

-  Makefile tox `#74 <https://github.com/Chyroc/WechatSogou/pull/74>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  fix typo `#69 <https://github.com/Chyroc/WechatSogou/pull/69>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Add tools test
   `#68 <https://github.com/Chyroc/WechatSogou/pull/68>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  fix import and mv tools function
   `#67 <https://github.com/Chyroc/WechatSogou/pull/67>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  update package
   `#66 <https://github.com/Chyroc/WechatSogou/pull/66>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add ci icon `#58 <https://github.com/Chyroc/WechatSogou/pull/58>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Add travis ci `#57 <https://github.com/Chyroc/WechatSogou/pull/57>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  release v2.0.3
   `#56 <https://github.com/Chyroc/WechatSogou/pull/56>`__
   (`Chyroc <https://github.com/Chyroc>`__)

`v2.0.3 <https://github.com/Chyroc/WechatSogou/tree/v2.0.3>`__ (2016-12-18)
---------------------------------------------------------------------------

**Closed issues:**

-  引入模块的时候报错
   `#33 <https://github.com/Chyroc/WechatSogou/issues/33>`__
-  导入文件后有bug
   `#31 <https://github.com/Chyroc/WechatSogou/issues/31>`__
-  请问如何设置代理
   `#27 <https://github.com/Chyroc/WechatSogou/issues/27>`__
-  请问最近搜狗返回的Html内容是改了吗？最近抓内容出错。
   `#25 <https://github.com/Chyroc/WechatSogou/issues/25>`__
-  结果模版更新了
   `#24 <https://github.com/Chyroc/WechatSogou/issues/24>`__
-  文章标题带引号（"，&quot）的情况解析报错
   `#23 <https://github.com/Chyroc/WechatSogou/issues/23>`__
-  请问，我运行test.py时为何没报错却没得到任何结果？
   `#21 <https://github.com/Chyroc/WechatSogou/issues/21>`__
-  如何获得公众号的id和名称？
   `#20 <https://github.com/Chyroc/WechatSogou/issues/20>`__
-  search\_gzh\_info无法取得内容
   `#18 <https://github.com/Chyroc/WechatSogou/issues/18>`__
-  原始文章url `#17 <https://github.com/Chyroc/WechatSogou/issues/17>`__
-  请问在Linux下可以使用吗？我运行了一下出现如下问题，还望指教
   `#16 <https://github.com/Chyroc/WechatSogou/issues/16>`__
-  log怎么使用？
   `#15 <https://github.com/Chyroc/WechatSogou/issues/15>`__
-  抓取数据有时成功，有时失败
   `#14 <https://github.com/Chyroc/WechatSogou/issues/14>`__
-  验证码打开失败问题原因是：
   `#13 <https://github.com/Chyroc/WechatSogou/issues/13>`__
-  验证码输入后失败
   `#12 <https://github.com/Chyroc/WechatSogou/issues/12>`__
-  获得的文章链接，如果打开需要验证码输入才跳转
   `#11 <https://github.com/Chyroc/WechatSogou/issues/11>`__
-  获取文章只能10篇？
   `#10 <https://github.com/Chyroc/WechatSogou/issues/10>`__
-  搜狗平台问题 `#9 <https://github.com/Chyroc/WechatSogou/issues/9>`__
-  deal\_article\_comment(text=text)并不能获得用户的评论内容
   `#8 <https://github.com/Chyroc/WechatSogou/issues/8>`__
-  py2.7 什么时候支持？
   `#7 <https://github.com/Chyroc/WechatSogou/issues/7>`__
-  PIL is not support Python3
   `#6 <https://github.com/Chyroc/WechatSogou/issues/6>`__
-  演示代码wechats.get\_gzh\_article\_by\_url\_dict(wechat\_info['url'])提示list
   index out of range
   `#5 <https://github.com/Chyroc/WechatSogou/issues/5>`__
-  如何使用代理 `#2 <https://github.com/Chyroc/WechatSogou/issues/2>`__
-  使用的是 python3 吗？
   `#1 <https://github.com/Chyroc/WechatSogou/issues/1>`__

**Merged pull requests:**

-  fix for ci `#50 <https://github.com/Chyroc/WechatSogou/pull/50>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add readme.rst
   `#48 <https://github.com/Chyroc/WechatSogou/pull/48>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  添加安装说明 `#47 <https://github.com/Chyroc/WechatSogou/pull/47>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  upload to pypi
   `#46 <https://github.com/Chyroc/WechatSogou/pull/46>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add `#45 <https://github.com/Chyroc/WechatSogou/pull/45>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Add/api test `#44 <https://github.com/Chyroc/WechatSogou/pull/44>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Fix/re ocr for get gzh article by url text
   `#43 <https://github.com/Chyroc/WechatSogou/pull/43>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  修复首页热门获取单页
   `#42 <https://github.com/Chyroc/WechatSogou/pull/42>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Fix/search article info
   `#41 <https://github.com/Chyroc/WechatSogou/pull/41>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Add/readme zanshu
   `#39 <https://github.com/Chyroc/WechatSogou/pull/39>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Fix/test ruokuai
   `#38 <https://github.com/Chyroc/WechatSogou/pull/38>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Feature/test ruokuai
   `#37 <https://github.com/Chyroc/WechatSogou/pull/37>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  Feature/update version
   `#35 <https://github.com/Chyroc/WechatSogou/pull/35>`__
   (`Chyroc <https://github.com/Chyroc>`__)
-  add requirements.txt
   `#34 <https://github.com/Chyroc/WechatSogou/pull/34>`__
   (`Chyroc <https://github.com/Chyroc>`__)

\* *This Change Log was automatically generated by
`github\_changelog\_generator <https://github.com/skywinder/Github-Changelog-Generator>`__*


