from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = settings.AUTH_USER_MODEL
from django.db import models
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from location_field.models.plain import PlainLocationField
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Instrument(models.Model):  
    INSTRUMENT_CHOICES = [
        ('Instrument non précisé', 'Instrument non précisé'),
        ('Clarinette sib solo', 'Clarinette sib solo'),
        ('Clarinette mib', 'Clarinette mib'),
        ('Clarinette sib 1', 'Clarinette sib 1'),
        ('Clarinette sib 2', 'Clarinette sib 2'),
        ('Clarinette sib 3A', 'Clarinette sib 3A'),
        ('Clarinette sib 3B', 'Clarinette sib 3B'),
        ('Clarinette sib 4', 'Clarinette sib 4'),
        ('Clarinette sib 5', 'Clarinette sib 5'),
        ('Clarinette basse 1A', 'Clarinette basse 1A'),
        ('Clarinette basse 1B', 'Clarinette basse 1B'),
        ('Clarinette basse 2', 'Clarinette basse 2'),
        ('Clarinette alto', 'Clarinette alto'),
        ('Cor de basset', 'Cor de basset'),
        ('Contrebasse à cordes', 'Contrebasse à cordes'),
        ('Trompette', 'Trompette'),
        ('Caisse claire', 'Caisse claire'),
        ('Grosse caisse', 'Grosse caisse'),
        ('Saxophone alto', 'Saxophone alto'),
        ('Saxophone baryton', 'Saxophone baryton'),
         ('Saxophone soprano', 'Saxophone soprano'),
        ('Saxophone ténor', 'Saxophone ténor'),
        ('Soubassophone', 'Soubassophone')
    ]
    title = models.CharField(max_length=200,
        choices=INSTRUMENT_CHOICES,default='Clarinette sib')
    class Meta:
        ordering = ('title',)
    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instruments = models.ManyToManyField(Instrument, related_name='profileinstruments')
    class Meta:
        verbose_name = u'Musicien'
        verbose_name_plural = u'Musiciens'
    def __str__(self):
        return '%s' % (self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Piece(models.Model):
    title = models.CharField(max_length=255)
    logo = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name="piecelogo")
    pdf  = FilerFileField(null=True, blank=True, on_delete=models.SET_NULL, related_name="piecepdf")
    mp3  = FilerFileField(null=True, blank=True, on_delete=models.SET_NULL, related_name="piecelink")
    link = models.CharField(null=True, blank=True, max_length=255)
    class Meta:
        ordering = ('title',)
    class Meta:
        verbose_name = u'Partition'
        verbose_name_plural = u'Partitions'
    def __str__(self):
        return self.title


class Location(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['address'], zoom=7)
    logo = FilerImageField(null=True, blank=True, on_delete=models.CASCADE, related_name="locationlogo")
    class Meta:
        ordering = ('title',)
    class Meta:
        verbose_name = u'Lieu'
        verbose_name_plural = u'Lieux'
    def __str__(self):
        return self.title


class Userinstrument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='instrumentuserinstruments')
    class Meta:
        ordering = ('user',)   
    class Meta:
        verbose_name = u'Musiciens : instrument possible'
        verbose_name_plural = u'Musiciens : instruments possibles'
    def __str__(self):
        return '%s %s' % (self.user,self.instrument)


class Event(models.Model):
    EVENT_TYPES = [
    ('PUBLIC', 'Evénement public'),
    ('PRIVE', 'Evénement privé'),
    ('REPET', 'Répétition'),  
    ]
    locations = models.ManyToManyField(Location, related_name='customevents')
    pieces = models.ManyToManyField(Piece, blank=True, related_name='eventpieces')
    instruments = models.ManyToManyField(Instrument, through='Eventinstrument', related_name='eventinstruments')
    stopvote = models.BooleanField('stop inscription', default=False)
    title= models.CharField(max_length=255)
    start = models.DateTimeField('Start')
    end = models.DateTimeField('End')
    all_day = models.BooleanField(('All day'), default=False)
    event_type = models.CharField(max_length=6,choices=EVENT_TYPES, default='REPET')
    note = models.TextField(default=False)
    manager = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        verbose_name = u'Evénement'
        verbose_name_plural = u'Evénements'
    def __str__(self):
        return '%s' % (self.title)


class Eventinstrument(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    nbmax = models.IntegerField(default=99)
    class Meta:
        ordering = ('event',)   
    class Meta:
        verbose_name = u'Evénement : max par instrument'
        verbose_name_plural = u'Evénements : max par instrument'
    def __str__(self):
        return '%s %s %s' % (self.event,self.instrument,self.nbmax)


class Participation(models.Model):
    PARTICIPATION_CHOICES = [
    ('OUI', 'J y serai'),
    ('NON', 'Je n y serai pas'),
    ('PEUT-ETRE', 'Je ne suis pas sûr'),  
    ]
    choice = models.CharField(max_length=9,choices=PARTICIPATION_CHOICES, default='OUI')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='eventparticipations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='instrumentparticipations')
    iswaiting = models.BooleanField('is waiting status', default=False)
    
    class Meta:
        ordering = ('instrument',)
        verbose_name = u'Inscription'
        verbose_name_plural = u'Inscriptions'

    def __str__(self):
        return '%s' % (self.instrument)