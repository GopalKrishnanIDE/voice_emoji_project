from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Recording
from .serializers import RecordingSerializer
from pydub import AudioSegment
import numpy as np
import os

def get_emoji_from_decibel(file_path):
    """
    Calculate approximate dB level and return an emoji.
    Works without audioop/pyaudioop (Render-friendly).
    """
    try:
        audio = AudioSegment.from_file(file_path)
        samples = np.array(audio.get_array_of_samples())
        rms = np.sqrt(np.mean(samples**2))
        db_level = 20 * np.log10(rms / (2**(8*audio.sample_width - 1))) if rms > 0 else -100
        print("Calculated dB level:", db_level)
    except Exception as e:
        print("Error reading audio:", e)
        db_level = -100  # fallback

    # Emoji assignment
    if db_level < -30:
        return "😢"
    elif -30 <= db_level < -10:
        return "🙂"
    elif -10 <= db_level < 0:
        return "😃"
    else:
        return "🤯"

class RecordingView(APIView):
    """
    API view to handle recording uploads and assign emoji.
    """
    def post(self, request):
        print('Recording under progress...')
        data = request.data.copy()
        audio_file = request.FILES.get('audio_file')

        if audio_file:
            temp_path = f"/tmp/{audio_file.name}"
            with open(temp_path, 'wb+') as temp_file:
                for chunk in audio_file.chunks():
                    temp_file.write(chunk)
            data['emoji'] = get_emoji_from_decibel(temp_path)
            os.remove(temp_path)
        else:
            data['emoji'] = "🙂"  # fallback

        serializer = RecordingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
