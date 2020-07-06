from django.urls import path, include

from appeal.views import AppealView
from notice.views import NoticeListView, NoticeUpdateView

app_name = "appeal"
urlpatterns = [
    path("submitAppeal/",AppealView.as_view(),name="submitAppeal")
]