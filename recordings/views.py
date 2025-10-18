from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Recording
from .serializers import RecordingSerializer
import wave
from pydub import AudioSegment
import audioop
import math


def get_emoji_from_decibel(file_path):
    """
    Calculate decibel level (dBFS) correctly and map to emoji.
    """
    try:
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_channels(1).set_frame_rate(44100)
        raw_data = audio.raw_data
        rms = audioop.rms(raw_data, audio.sample_width)

        # Correct normalization: reference value depends on sample width
        max_possible_amplitude = float(1 << (8 * audio.sample_width - 1))
        db_level = 20 * math.log10(rms / max_possible_amplitude) if rms > 0 else -90
        print(f"Calculated dB level: {db_level:.2f} dBFS")
    except Exception as e:
        print("Error reading audio:", e)
        db_level = -90

    # Adjusted thresholds
    if db_level < -45:
        emoji = "😢"  # very quiet
    elif -45 <= db_level < -30:
        emoji = "🙂"  # normal
    elif -30 <= db_level < -15:
        emoji = "😃"  # loud
    else:
        emoji = "🤯"  # very loud / clipping

    print(f"Assigned emoji: {emoji}")
    return emoji

class RecordingView(APIView):
    """
    API view to handle recording uploads and assign emoji based on decibel.
    """
    def post(self, request):
        print('Recording under progress...')
        data = request.data.copy()

        # Temporarily save uploaded file to calculate decibel
        audio_file = request.FILES.get('audio_file')
        if audio_file:
            temp_path = f"/tmp/{audio_file.name}"
            with open(temp_path, 'wb+') as temp_file:
                for chunk in audio_file.chunks():
                    temp_file.write(chunk)
            # Assign emoji based on decibel level
            data['emoji'] = get_emoji_from_decibel(temp_path)
        else:
            data['emoji'] = "🙂"  # fallback

        serializer = RecordingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
