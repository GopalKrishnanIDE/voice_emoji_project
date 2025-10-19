from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from django.core.files.storage import default_storage

class RecordingView(APIView):
    def get(self, request):
        return Response({"status": "OK", "message": "GET request received successfully"})

    def post(self, request):
        audio_file = request.FILES.get("audio_file")
        if not audio_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save uploaded file
        file_name = default_storage.save(audio_file.name, audio_file)
        audio_url = f"{request.build_absolute_uri('/media/' + file_name)}"
        
        # Example emoji generation
        emoji = "😊"

        return Response({"emoji": emoji, "audio_file": audio_url})