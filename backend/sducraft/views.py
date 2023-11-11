from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from django.db import transaction
from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

###proxyserver###
class ProxyServerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProxyServer
        fields="__all__"

class ProxyServerView(ReadOnlyModelViewSet):
    queryset=ProxyServer.objects.all().order_by('rank')
    serializer_class=ProxyServerSerializer

 #img for proxyserver#
class ImageSetForProxyServerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageSetForProxyServer
        exclude = ('random_string','publish_date','modify_date')

class ImageSetForProxyServerView(ReadOnlyModelViewSet):
    queryset=ImageSetForProxyServer.objects
    serializer_class=ImageSetForProxyServerSerializer
    
###server###
class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Server
        fields="__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['init_date'] = data['init_date'][:10]
        if data['close_date']:
            data['close_date'] = data['close_date'][:10]
        else:
            data['close_date']='unknown'
        return data

class ServerView(ReadOnlyModelViewSet):
    queryset=Server.objects.all().order_by('rank')
    serializer_class=ServerSerializer

    def filter_queryset(self,queryset):
        #插入的部分
        ProxyServerId=self.request.GET.get("proxyserver",None)
        if ProxyServerId is not None:
            return queryset.filter(proxyServer=ProxyServerId)
        #下面是原函数filter_queryset
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
    
 #img for server#
class ImageSetForServerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageSetForServer
        exclude = ('random_string','publish_date','modify_date')

class ImageSetForServerView(ReadOnlyModelViewSet):
    queryset=ImageSetForServer.objects
    serializer_class=ImageSetForServerSerializer

###vmember
class VTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model=VTeam
        fields = '__all__'

class VTeamView(ReadOnlyModelViewSet):
    queryset=VTeam.objects.all().order_by('rank')
    serializer_class=VTeamSerializer

class VGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=VGroup
        fields = '__all__'

class VGroupView(ReadOnlyModelViewSet):
    queryset=VGroup.objects.all().order_by('rank')
    serializer_class=VGroupSerializer

class VMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=VMember
        exclude = ('random_string','publish_date','modify_date')

class VMemberView(ReadOnlyModelViewSet):
    queryset=VMember.objects.all().order_by('rank')
    serializer_class=VMemberSerializer

###history###
class HistoryNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=HistoryNode
        exclude = ('history','name')

class HistoryNodeView(ReadOnlyModelViewSet):
    queryset=HistoryNode.objects.all().order_by('-date')
    serializer_class=HistoryNodeSerializer
    
 #img for history#
class ImageSetForHistoryNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageSetForHistoryNode
        exclude = ('random_string','publish_date','modify_date')

class ImageSetForHistoryNodeView(ReadOnlyModelViewSet):
    queryset=ImageSetForHistoryNode.objects
    serializer_class=ImageSetForHistoryNodeSerializer

###notice###
class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notice
        exclude = ('file','random_string')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['publish_date']:
            data['publish_date'] = data['publish_date'][:10]
        if data['modify_date']:
            data['modify_date'] = data['modify_date'][:10]
        return data

class NoticeView(ReadOnlyModelViewSet):
    queryset=Notice.objects.all().order_by('-publish_date')
    serializer_class=NoticeSerializer
    
###download###
class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Download
        exclude = ('random_string',)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['publish_date']:
            data['publish_date'] = data['publish_date'][:10]
        if data['modify_date']:
            data['modify_date'] = data['modify_date'][:10]
        return data

class DownloadView(ReadOnlyModelViewSet):
    queryset=Download.objects.all().order_by('rank')
    serializer_class=DownloadSerializer
    
class FileSetForDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model=FileSetForDownload
        exclude = ('random_string',)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['publish_date']:
            data['publish_date'] = data['publish_date'][:10]
        if data['modify_date']:
            data['modify_date'] = data['modify_date'][:10]
        return data

class FileSetForDownloadView(ReadOnlyModelViewSet):
    queryset=FileSetForDownload.objects.all().order_by('rank')
    serializer_class=FileSetForDownloadSerializer
    
###intro###
class IntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Introduction
        exclude = ('file','random_string')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['publish_date']:
            data['publish_date'] = data['publish_date'][:10]
        if data['modify_date']:
            data['modify_date'] = data['modify_date'][:10]
        return data

class IntroductionView(ReadOnlyModelViewSet):
    queryset=Introduction.objects.all().order_by('rank')
    serializer_class=IntroductionSerializer
    
###doc###
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Document
        exclude = ('file','random_string')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['publish_date']:
            data['publish_date'] = data['publish_date'][:10]
        if data['modify_date']:
            data['modify_date'] = data['modify_date'][:10]
        return data

class DocumentView(ReadOnlyModelViewSet):
    queryset=Document.objects.all().order_by('-publish_date')
    serializer_class=DocumentSerializer
    
###activity###
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Activity
        exclude = ('file','random_string')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['publish_date']:
            data['publish_date'] = data['publish_date'][:10]
        if data['modify_date']:
            data['modify_date'] = data['modify_date'][:10]
        data['img']=ImageSetForActivitySerializer(instance.imagesetforactivity_set.all(), many=True).data
        return data

class ActivityView(ReadOnlyModelViewSet):
    queryset=Activity.objects.all().order_by('-publish_date')
    serializer_class=ActivitySerializer
    
    #据说能保证原子性
    @transaction.atomic
    def increase_clicks(self, instance):
        instance.clicks += 1
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id:
            self.increase_clicks(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
 #img for activity#
class ImageSetForActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageSetForActivity
        exclude = ('random_string','publish_date','modify_date')

class ImageSetForActivityView(ReadOnlyModelViewSet):
    queryset=ImageSetForActivity.objects
    serializer_class=ImageSetForActivitySerializer

    def filter_queryset(self,queryset):
        #插入的部分
        ActivityID=self.request.GET.get("activityid",None)
        if ActivityID is not None:
            return Activity.objects.get(id=ActivityID).imagesetforactivity_set.all()
            # return queryset.filter(proxyServer=ActivityID)
        #下面是原函数filter_queryset
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset