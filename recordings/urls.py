from django.urls import path
from .views import RecordingView

urlpatterns = [
    path("recordings/", RecordingView.as_view(), name="recordings"),
]
