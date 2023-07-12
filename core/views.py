from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
import json
import pafy
import tempfile
import os
import yt_dlp as youtube_dl
# import youtube_dl

def main(request):
    return render(request, 'main.html')


@csrf_exempt
def download_video(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			video_url = data.get('url')
			quality = data.get('quality', '192')
			print(video_url, quality, 'url + quality')
			ydl_opts = {
				'format': 'bestaudio/best',
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': quality,
				}],
			}

			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				info = ydl.extract_info(video_url, download=False)
				audio_url = info['formats'][0]['url']
				audio_file = ydl.prepare_filename(info)
				ydl.download([video_url])
			
			response = FileResponse(open(audio_file, 'rb'), content_type='audio/mp3')
			response['Content-Disposition'] = 'attachment; filename="audio.mp3"'

			return response
		except json.JSONDecodeError:
			return HttpResponse("Invalid JSON")
	else:
		return HttpResponse('Invalid request method')