from django.contrib import admin
from .models import *
import nested_admin

#server
class ImageSetForServerInline(nested_admin.NestedTabularInline):
    model=ImageSetForServer
    fields = ('img',) 
    extra=1

class ServerInline(nested_admin.NestedStackedInline):
    model=Server
    extra=1
    inlines=[ImageSetForServerInline]

class ImageSetForProxyServerInline(nested_admin.NestedTabularInline):
    model=ImageSetForProxyServer
    fields = ('img',)
    extra=1

class ProxyServerAdmin(nested_admin.NestedModelAdmin):
    exclude=[]
    inlines=[ImageSetForProxyServerInline,ServerInline]

class ServerAdmin(nested_admin.NestedModelAdmin):
    exclude=[]

#vmember
class VMemberInline(nested_admin.NestedStackedInline):
    model=VMember
    fields=['campus','school','grade','major','name','img','rank']
    extra=1

class VGroupInline(nested_admin.NestedStackedInline):
    model=VGroup
    extra=1
    inlines=[VMemberInline]
    fields=['group_name','rank']

class VTeamAdmin(nested_admin.NestedModelAdmin):
    inlines=[VGroupInline]
    fields=['team_name','date','rank']

#history
class ImageSetForHistoryNodeInline(nested_admin.NestedTabularInline):
    model=ImageSetForHistoryNode
    fields = ('img',"name") 
    extra=1

class HistoryNodeInline(nested_admin.NestedStackedInline):
    inlines=[ImageSetForHistoryNodeInline]
    model=HistoryNode
    extra=1
    fields=['name','level','date','content']

class HistoryAdmin(nested_admin.NestedModelAdmin):
    inlines=[HistoryNodeInline]
    fields=['name',]

#notice
class NoticeAdmin(admin.ModelAdmin):
    readonly_fields=['modify_date','front_end_address']
    fieldsets = [
        (None, {"fields": ["publish_date",'modify_date','invalid_date','front_end_address',"title","author","valid"]}),
        ("公告上传：请将md文件以及引用的图片（仅支持相对路径引用图片）打包成.zip文件上传。", {"fields": ["file"]}),
    ]

class FileSetForDownloadInline(nested_admin.NestedStackedInline):
    model=FileSetForDownload
    readonly_fields=['publish_date','modify_date','size']
    fields=['OS','size','file','rank']
    extra=1

class DownloadAdmin(nested_admin.NestedModelAdmin):
    readonly_fields=['modify_date',]
    fields=['publish_date','modify_date','name','version','intro','img','rank','author']
    inlines=[FileSetForDownloadInline]

class IntroductionAdmin(admin.ModelAdmin):
    readonly_fields=['front_end_address']
    fieldsets = [
        (None, {"fields": ["publish_date",'modify_date','front_end_address',"title","author","rank"]}),
        ("介绍页面上传：请将md文件以及引用的图片（仅支持相对路径引用图片）打包成.zip文件上传。", {"fields": ["file"]}),
    ]

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields=['front_end_address']
    fieldsets = [
        (None, {"fields": ["publish_date",'modify_date','front_end_address',"title","author","rank"]}),
        ("文档页面上传：请将md文件以及引用的图片（仅支持相对路径引用图片）打包成.zip文件上传。", {"fields": ["file"]}),
    ]

class ImageSetForActivityInline(nested_admin.NestedTabularInline):
    model=ImageSetForActivity
    fields = ('img',) 
    extra=1

class ActivityAdmin(nested_admin.NestedModelAdmin):
    readonly_fields=['front_end_address','summary']
    fieldsets = [
        (None, {"fields": ["publish_date",'modify_date','front_end_address',"title","author","summary","rank","clicks"]}),
        ("文档页面上传：请将md文件以及引用的图片（仅支持相对路径引用图片）打包成.zip文件上传。", {"fields": ["file"]}),
    ]
    inlines=[ImageSetForActivityInline]

admin.site.register(ProxyServer,ProxyServerAdmin)
admin.site.register(Server,ServerAdmin)
admin.site.register(Notice,NoticeAdmin)
admin.site.register(Download,DownloadAdmin)
admin.site.register(VTeam,VTeamAdmin)
admin.site.register(History,HistoryAdmin)
admin.site.register(Introduction,IntroductionAdmin)
admin.site.register(Document,DocumentAdmin)
admin.site.register(Activity,ActivityAdmin)