from django.urls import path
from .views import RecordingView

urlpatterns = [
    path('', RecordingView.as_view(), name="recordings"),  # empty string, not "recordings/"
]
