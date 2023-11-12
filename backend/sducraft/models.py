from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

import mistune
from bs4 import BeautifulSoup

import os
import zipfile
import shutil
import random
import string

MINLEN=16
MIDLEN=32
LARLEN=64

def getRandomString(length=16):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def custom_upload_path(instance, fileName):
    return instance.files_directory+fileName

class FileAbstract(models.Model):
    random_string=models.CharField(max_length=MIDLEN,default=getRandomString)
    publish_date=models.DateTimeField(default=timezone.now)
    modify_date=models.DateTimeField(blank=True,null=True)
    # 在fileSet注册文件字段
    fileSet=[]

    # 声明该类为抽象类
    class Meta:
        abstract = True
    
    @property
    def files_directory(self):
        return self.__class__.__name__+'/'+self.publish_date.strftime("%Y-%m-%d")+'/'+self.random_string+'/'

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        # 该实例是否存在于数据库中
        for fileItemString in self.__class__.fileSet:
            file_instance=getattr(self,fileItemString)
            if self.pk:
                if file_instance.name.startswith(self.__class__.__name__):
                    pass
                elif file_instance.name=='':
                    # 实现清除功能
                    try:
                        old_instance = self.__class__.objects.get(pk=self.pk)
                        old_file_instance=getattr(old_instance,fileItemString)
                        # 能拿到对象说明正在进行清除（即上传为空，后端有内容），需要删
                        # 拿不到对象说明从来没有上传过文件（上传为空，后端无内容），连文件都没有，不用删
                        if old_file_instance and os.path.exists(old_file_instance.path):
                            os.remove(old_file_instance.path)
                    except Exception as e:
                        pass
                else:
                    # 上传了新文件
                    try:
                        old_instance = self.__class__.objects.get(pk=self.pk)
                        old_file_instance=getattr(old_instance,fileItemString)
                        if old_file_instance and os.path.exists(old_file_instance.path):
                            # 删除旧文件
                            os.remove(old_file_instance.path)
                    except Exception as e:
                        pass

        # 更新修改时间
        self.modify_date=timezone.now()
        tmp=super().save(force_insert, force_update, using, update_fields)
        return tmp
    
    def delete(self, using=None, keep_parents=False):
        tmp=super().delete(using, keep_parents)
        # 删除文件
        path=settings.MEDIA_ROOT+self.files_directory
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                pass
        # 如果同一天没有其它文件，删除目录
        path=settings.MEDIA_ROOT+'/'.join(self.files_directory.split('/')[:-2])
        if os.path.exists(path):
            if not os.listdir(path):
                os.rmdir(path)
        return tmp

class FileBase(FileAbstract):
    file=models.FileField(blank=True, null=True,upload_to=custom_upload_path)
    fileSet=['file',]
    class Meta:
        abstract = True

class ImgBase(FileAbstract):
    img=models.ImageField(blank=True, null=True,upload_to=custom_upload_path)
    fileSet=['img',]
    class Meta:
        abstract = True

class FileImgMixin(FileAbstract):
    file=models.FileField(blank=True, null=True,upload_to=custom_upload_path)
    img=models.ImageField(blank=True, null=True,upload_to=custom_upload_path)
    fileSet=['file','img']
    class Meta:
        abstract = True

class ZipFileBase(FileBase):
    front_end_address=models.CharField(max_length=LARLEN,blank=True,null=True,default="nowhere")
    file=models.FileField(upload_to=custom_upload_path)
    class Meta:
        abstract = True

    @property
    def front_files_directory(self):
        return settings.FRONT+self.files_directory
    
    def beforeSaving(self, content, name):
        return content,name

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        if self.pk and (self.file.name.startswith(self.__class__.__name__) or self.file.name==''):
            if self.file.name.startswith(self.__class__.__name__):
                pass
            elif self.file.name=='':
                # 实现清除功能
                try:
                    old_file_instance = self.__class__.objects.get(pk=self.pk).file
                    # 能拿到对象说明正在进行清除（即上传为空，后端有内容），需要删
                    # 拿不到对象说明从来没有上传过文件（上传为空，后端无内容），连文件都没有，不用删
                    if old_file_instance:
                        old_file_path=settings.MEDIA_ROOT+old_file_instance.front_files_directory
                        if os.path.exists(old_file_path):
                            try:
                                shutil.rmtree(old_file_path)
                            except Exception as e:
                                pass
                        old_file_instance.front_end_address='nowhere'
                        # 如果同一天没有其它文件，删除目录
                        path=settings.MEDIA_ROOT+'/'.join(self.front_files_directory.split('/')[:-2])
                        if os.path.exists(path):
                            if not os.listdir(path):
                                os.rmdir(path)     
                except Exception as e:
                    pass
        #上传了文件
        else:
            #处理带有md文件的zip文件
            if(self.file.name.endswith('zip')):
                #获取.zip文件
                file_instance=self.file.file
                with zipfile.ZipFile(file_instance, 'r') as zip_ref:
                    # 获取.zip文件中的文件列表
                    file_list = zip_ref.namelist()
                    #检查上传的.zip文件是否合法,即有md文件
                    successs=False
                    for file_name in file_list:
                        if file_name.endswith('.md') or file_name.endswith('.html'):
                            successs=True  
                            break
                    #zip文件合法，删除可能存在的旧文件，开始新文件的部署
                    if successs:
                        #删除旧文件
                        old_file_path=settings.MEDIA_ROOT+self.front_files_directory
                        if os.path.exists(old_file_path):
                            try:
                                shutil.rmtree(old_file_path)
                            except Exception as e:
                                pass
                        #删除完毕，开始部署
                        for file_name in file_list:
                            # 修复mac可能导致的问题
                            if file_name.endswith('/') or '__MACOSX' in file_name:
                                continue
                            # 使用open()函数打开文件对象，然后读取其内容(从压缩文件中提取文件)
                            with zip_ref.open(file_name) as extracted_file:
                                file_contents = extracted_file.read()
                                # 如果是.md文件，记录为前端地址
                                if file_name.endswith('.md') or file_name.endswith('.html'):
                                    file_contents,file_name=self.beforeSaving(file_contents,file_name)
                                    self.front_end_address=self.front_files_directory+file_name
                                # 写入目标路径
                                target_file_path=settings.MEDIA_ROOT+self.front_files_directory+file_name
                                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                                with open(target_file_path, 'wb') as target_file:
                                    target_file.write(file_contents)
                    #报错，中止程序
                    else:
                        raise FileNotFoundError('压缩包中必须带有md或html文件！')
                            
            #其它文件
            else:
                #删除旧文件
                old_file_path=settings.MEDIA_ROOT+self.front_files_directory
                if os.path.exists(old_file_path):
                    try:
                        shutil.rmtree(old_file_path)
                    except Exception as e:
                        pass
                #写前准备
                file_contents=self.file.file.read()
                file_contents,file_name=self.beforeSaving(file_contents,self.file.name)
                #构造地址
                self.front_end_address=self.front_files_directory+file_name
                target_file_path=settings.MEDIA_ROOT+self.front_end_address
                #写入文件
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                with open(target_file_path, 'wb') as target_file:
                    target_file.write(file_contents)

        tmp=super().save(force_insert, force_update, using, update_fields)
        return tmp

    def delete(self, using=None, keep_parents=False):
        tmp=super().delete(using, keep_parents)
        # 删除前端文件
        old_file_path=settings.MEDIA_ROOT+self.front_files_directory
        if os.path.exists(old_file_path):
            try:
                shutil.rmtree(old_file_path)
            except Exception as e:
                pass
        # 如果同一天没有其它文件，删除目录
        path=settings.MEDIA_ROOT+'/'.join(self.front_files_directory.split('/')[:-2])
        if os.path.exists(path):
            if not os.listdir(path):
                os.rmdir(path)

        return tmp
    
    

class ProxyServer(models.Model):
    name=models.CharField(max_length=MINLEN)
    version=models.CharField(max_length=MIDLEN)
    host=models.CharField(max_length=MIDLEN)
    port=models.IntegerField()
    intro=models.TextField()
    rank=models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name
    
class ImageSetForProxyServer(ImgBase):
    proxyServer=models.ForeignKey(ProxyServer,on_delete=models.CASCADE)

class Server(models.Model):
    MODE_CHOICES=[
        ("survival","survival"),
        ("creative","creative"),
        ("adventure","adventure"),
        ("spectator","spectator"),
        ("hardcore","hardcore"),
    ]
    proxyServer=models.ForeignKey(ProxyServer,on_delete=models.CASCADE)
    name=models.CharField(max_length=MINLEN)
    mode=models.CharField(max_length=MINLEN,choices=MODE_CHOICES,default="survival")
    version=models.CharField(max_length=MIDLEN)
    host=models.CharField(max_length=MIDLEN,blank=True,null=True)
    port=models.IntegerField(blank=True,null=True)
    bridge_name=models.CharField(max_length=MINLEN,blank=True,null=True)
    author=models.CharField(max_length=MIDLEN,blank=True,null=True)
    init_date=models.DateTimeField()
    close_date=models.DateTimeField(blank=True,null=True)
    intro=models.TextField()
    rank=models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name
    
class ImageSetForServer(ImgBase):
    server=models.ForeignKey(Server,on_delete=models.CASCADE)


class Notice(ZipFileBase):
    VALID_CHOICES=[
        (0,"无效"),
        (1,"有效"),
        (2,"置顶"),
        (3,"重要"),
    ]
    title=models.CharField(max_length=MIDLEN,blank=True,null=True)
    author=models.CharField(max_length=MIDLEN,blank=True,null=True)
    valid=models.IntegerField(choices=VALID_CHOICES,default=1)
    invalid_date=models.DateTimeField(blank=True,null=True)

    def __str__(self) -> str:
        if(self.title==None):
            return "null"
        return self.title

class Download(ImgBase):
    name=models.CharField(max_length=MIDLEN,blank=True,null=True)
    version=models.CharField(max_length=MIDLEN,blank=True,null=True)
    intro=models.TextField(blank=True,null=True)
    rank=models.IntegerField(default=0)
    author=models.CharField(max_length=MIDLEN,blank=True,null=True)
    
    def __str__(self) -> str:
        if(self.name==None):
            return "null"
        return self.name
    
class FileSetForDownload(FileBase):
    OS_CHOICES=[
        ('Windows','Windows'),
        ('Mac','Mac'),
        ('Linux','Linux')
    ]
    OS=models.CharField(max_length=MINLEN,choices=OS_CHOICES,default='Windows')
    download=models.ForeignKey(Download,on_delete=models.CASCADE)
    size=models.FloatField(blank=True,null=True)
    rank=models.IntegerField(default=0)

    def __str__(self) -> str:
        if(self.OS==None):
            return "null"
        return self.OS
    
    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        #修改文件大小
        try:
            self.file.file.seek(0, 2)
            file_size = self.file.file.tell()
            self.size=round(file_size/(1024*1024),3)
        except Exception as e:
            self.size=0
        tmp=super().save(force_insert, force_update, using, update_fields)
        return tmp
    
class VTeam(models.Model):
    team_name=models.CharField(max_length=MIDLEN,blank=True,null=True)
    date=models.DateTimeField(default=timezone.now)
    rank=models.IntegerField(default=0)
    
    def __str__(self) -> str:
        if(self.team_name==None):
            return "null"
        return self.team_name

class VGroup(models.Model):
    team_id=models.ForeignKey(VTeam,on_delete=models.PROTECT)
    group_name=models.CharField(max_length=MIDLEN,blank=True,null=True)
    rank=models.IntegerField(default=0)

    def __str__(self) -> str:
        if(self.group_name==None):
            return "null"
        return self.group_name

class VMember(ImgBase):
    group_id=models.ForeignKey(VGroup,on_delete=models.CASCADE)

    name=models.CharField(max_length=MIDLEN,blank=True,null=True)
    campus=models.CharField(max_length=MINLEN,blank=True,null=True)
    school=models.CharField(max_length=MINLEN,blank=True,null=True)
    grade=models.IntegerField(default=1901)
    major=models.CharField(max_length=MINLEN,blank=True,null=True)
    rank=models.IntegerField(default=0)

    def __str__(self) -> str:
        if(self.name==None):
            return "null"
        return self.name
    
class History(models.Model):
    name=models.CharField(max_length=MIDLEN,blank=True,null=True)

    def __str__(self) -> str:
        if(self.name==None):
            return "null"
        return self.name

class HistoryNode(models.Model):
    LEVEL_CHOICES=[
        (0,"一般"),
        (1,"重要"),
    ]
    history=models.ForeignKey(History,on_delete=models.CASCADE)
    name=models.CharField(max_length=MIDLEN,blank=True,null=True)
    level=models.IntegerField(choices=LEVEL_CHOICES,default=0)
    date=models.DateTimeField(default=timezone.now)
    content=models.TextField(blank=True,null=True)

    def __str__(self) -> str:
        if(self.name==None):
            return "null"
        return self.name
    
class ImageSetForHistoryNode(ImgBase):
    historynode=models.ForeignKey(HistoryNode,on_delete=models.CASCADE)
    name=models.CharField(max_length=MIDLEN,blank=True,null=True)
    
class Introduction(ZipFileBase):
    title=models.CharField(max_length=MIDLEN,blank=True,null=True)
    author=models.CharField(max_length=MIDLEN,blank=True,null=True)
    rank=models.IntegerField(default=0)

    def __str__(self) -> str:
        if(self.title==None):
            return "null"
        return self.title
    
class Document(ZipFileBase):
    title=models.CharField(max_length=MIDLEN,blank=True,null=True)
    author=models.CharField(max_length=MIDLEN,blank=True,null=True)
    rank=models.IntegerField(default=0)

    def __str__(self) -> str:
        if(self.title==None):
            return "null"
        return self.title
    
class Activity(ZipFileBase):
    title=models.CharField(max_length=MIDLEN,blank=True,null=True)
    author=models.CharField(max_length=MIDLEN,blank=True,null=True)
    summary=models.TextField(blank=True,null=True)
    rank=models.IntegerField(default=0)
    clicks=models.IntegerField(default=0)
    wordCount=models.IntegerField(default=0)

    def __str__(self) -> str:
        if(self.title==None):
            return "null"
        return self.title
    
    def beforeSaving(self, content, name):
        #全部转成html
        content_ascii=content.decode('utf-8')
        if(name.endswith('.md')):
            content_ascii = mistune.html(content_ascii)
            content=content_ascii.encode('utf-8')
            name=name[:-2]+'html'
        #提取纯文本，设置摘要
        soup = BeautifulSoup(content_ascii, 'html.parser')
        text_content = soup.get_text()
        self.wordCount=len(text_content)
        if(self.wordCount>=50):
            self.summary=text_content[0:50]+"..."
        else:
            self.summary=text_content
        #返回
        return content,name

class ImageSetForActivity(ImgBase):
    activity=models.ForeignKey(Activity,on_delete=models.CASCADE)