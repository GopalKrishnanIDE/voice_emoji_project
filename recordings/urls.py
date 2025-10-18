from django.urls import path
from .views import RecordingView

urlpatterns = [
    path('record/', RecordingView.as_view(), name='recording'),
]
