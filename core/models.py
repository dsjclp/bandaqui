from django.db import models
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from animation.models import Event

class Photo(models.Model):
    title= models.CharField(max_length=255)
    picture = FilerImageField(on_delete=models.CASCADE, related_name="eventpicture")
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True, related_name='galleryitsphotos')

    class Meta:
        ordering = ('title',)
        verbose_name = u'Photo'
        verbose_name_plural = u'Photos'

    def __str__(self):
        return self.title
    

class Video(models.Model):
    title= models.CharField(max_length=255)
    video = FilerFileField(on_delete=models.CASCADE, related_name="eventvideo")
    poster = FilerImageField(on_delete=models.SET_NULL, blank=True, null=True, related_name="eventvideoposter")
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True, related_name='galleryitsvideos')

    class Meta:
        ordering = ('title',)
        verbose_name = u'Vidéo'
        verbose_name_plural = u'Vidéos'

    def __str__(self):
        return self.title