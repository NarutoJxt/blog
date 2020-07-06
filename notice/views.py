from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin



class NoticeListView(ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/notice.html'
    # 登录重定向
    paginate_by = 10

    # 未读通知的查询集
    def get_queryset(self):
        q = self.request.user.notifications.order_by("-unread")
        get_type = self.request.GET.get("type")
        try:
            q = q.filter(description=get_type)
        except KeyError as e:
            q = None
        return q
    def get_context_data(self, *, object_list=None, **kwargs):
        header = {"comment": "评论", "collection": "收藏", "attention": "关注","appeal":"投诉","other":"其他"}
        context = super(NoticeListView,self).get_context_data(**kwargs)
        context["show"] = header[self.request.GET.get("type")]
        context["type"] = self.request.GET.get("type")
        return context


class NoticeUpdateView(View):
    """更新通知状态"""
    # 处理 get 请求
    def get(self, request):
        # 获取未读消息
        get_type = request.GET.get('type')
        way = request.GET.get("way")
        al_way = request.GET.get("al_way")
        # 更新单条通知
        if way == "all":
            if al_way == "delete":
                request.user.notifications.filter(description=get_type).delete()
            else:
                request.user.notifications.filter(description=get_type).mark_all_as_read()
        elif way == "simple":
            pk = request.GET.get("pk")
            request.user.notifications.get(pk=pk).delete()
        elif way == "read":
            pk = request.GET.get("pk")
            request.user.notifications.get(pk=pk).mark_as_read()
        elif way == "unread":
            pk = request.GET.get("pk")
            request.user.notifications.get(pk=pk).mark_as_unread()
        url = reverse("notice:show") + "?type=" + get_type
        return HttpResponseRedirect(url)