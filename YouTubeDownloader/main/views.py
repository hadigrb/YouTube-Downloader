from django.shortcuts import render,redirect
from django.views.generic import View
from pytube import *
import sys

class home(View):
    def __init__(self,url=None):
        self.url = url
    def get(self,request):
        return render(request,'main/home.html')
    def post(self,request):
        if request.POST.get('fetch-vid'):
            self.url = request.POST.get('given_url')
            video = YouTube(self.url)
            video_title , video_thumbnail = video.title , video.thumbnail_url
            qual , stream = [] , []
            for vid in video.streams.filter(progressive=True):
                qual.append(vid.resolution)
                stream.append(vid)
            context = {
                'video_title':video_title,
                'video_thumbnail':video_thumbnail,
                'qual':qual,
                'stream':stream,
                'url':self.url
            }
            return render(request,'main/home.html',context=context)
        
        elif request.POST.get('download-vid'):
            self.url = request.POST.get('given_url')
            video = YouTube(self.url)
            stream = [x for x in video.streams.filter(progressive=True)]
            choosen_qual = video.streams[int(request.POST.get('download-vid')) - 1]
            choosen_qual.download(output_path='../../Downloads')
            sys.exit()
            return redirect('home')
        return render(request,'main/home.html')
