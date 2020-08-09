# djangoBlog
一个在线博客系统，使用python的Django框架实现，实现了包括用户认证，文章管理，搜索，缓存，文本编辑等等一系列的功能。
 主要使用的技术如下：
1. haystack+elasticsearch实现搜索
2. redis实现缓存
3. froala实现富文本编辑
4. django-notifycation实现消息通知
5. bootstrap实现前端界面

# 安装步骤
1. pip install requirements.txt
2. 由于使用新版django，经常会出现django.utils包下找不到six模块，只需将six.py复制到utils包下即可。
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py rebuild_index
6. python manage.py collectstatic
7. python manage.runserver

