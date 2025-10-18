from rest_framework.views import APIView
from rest_framework.response import Response

class RecordingView(APIView):
    def get(self, request):
        return Response({"status": "OK", "message": "GET request received successfully"})
