from django.db import models

class Recording(models.Model):
    audio_file = models.FileField(upload_to='recordings/')
    emoji = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emoji} at {self.timestamp}"
from django.db import models

# Create your models here.
