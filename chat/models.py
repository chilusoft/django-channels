from django.db import models

# Create your models here.

class ChannelName(models.Model):
    channel_name = models.CharField(max_length=100, null=True, blank=True)
    channel_description = models.CharField(max_length=100, null=True, blank=True)
    # channel_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.channel_name