from django.urls import path

from . import views

from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("proxyserver",views.ProxyServerView)
router.register("imagesetforproxyserver",views.ImageSetForProxyServerView)
router.register("server",views.ServerView)
router.register("imagesetforserver",views.ImageSetForServerView)
router.register("notice",views.NoticeView)
router.register("download",views.DownloadView)
router.register("vteam",views.VTeamView)
router.register("vgroup",views.VGroupView)
router.register("vmember",views.VMemberView)
router.register("historynode",views.HistoryNodeView)
router.register("imagesetforhistorynode",views.ImageSetForHistoryNodeView)
router.register("filesetfordownload",views.FileSetForDownloadView)
router.register("introduction",views.IntroductionView)
router.register("document",views.DocumentView)
router.register("activity",views.ActivityView)
router.register("imagesetforactivity",views.ImageSetForActivityView)


urlpatterns = [
    path("", views.index, name="index"),
]
urlpatterns+=router.urls