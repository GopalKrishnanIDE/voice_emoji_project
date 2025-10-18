from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Recording
from .serializers import RecordingSerializer
from pydub import AudioSegment  # Safe, we will only use basic features
import numpy as np
import os

def get_emoji_from_decibel(file_path):
    """
    Pure numpy-based dB calculation without audioop/pyaudioop.
    """
    try:
        audio = AudioSegment.from_file(file_path)
        samples = np.array(audio.get_array_of_samples())
        rms = np.sqrt(np.mean(samples**2))
        db_level = 20 * np.log10(rms / (2**(8*audio.sample_width - 1))) if rms > 0 else -100
    except Exception as e:
        print("Error reading audio:", e)
        db_level = -100

    if db_level < -30:
        return "😢"
    elif -30 <= db_level < -10:
        return "🙂"
    elif -10 <= db_level < 0:
        return "😃"
    else:
        return "🤯"

class RecordingView(APIView):
    def post(self, request):
        data = request.data.copy()
        audio_file = request.FILES.get('audio_file')

        if audio_file:
            temp_path = f"/tmp/{audio_file.name}"
            with open(temp_path, 'wb+') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
            data['emoji'] = get_emoji_from_decibel(temp_path)
            os.remove(temp_path)
        else:
            data['emoji'] = "🙂"

        serializer = RecordingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
