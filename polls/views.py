from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import json
import openai
from pytube import YouTube
import os

class HomeView(View):
    def get(self, request):
        return HttpResponse({'home': 'Home'})
    
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        urll = body['yt_url']
        video = YouTube(urll)
        filename = video.title
        audios = video.streams.filter(only_audio=True)
        audios[-1].download()
        audio_file= open("./{}.webm".format(filename), "rb")
        openai.api_key = "your api key"
        transcript = openai.Audio.translate("whisper-1", audio_file)
        summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": "Please summarize the text. {}".format(transcript)},
                ]
            )
        audio_file.close()
        os.remove("./{}.webm".format(filename))
        return HttpResponse(summary['choices'][0]['message']['content'])