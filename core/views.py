from django.views import generic
from django.utils import timezone
from .models import Photo
from .models import Video
from animation.models import Event
from blog.models import Post
from django.contrib import messages
from .util import events_to_json
from django.http import HttpResponse


class HomePage(generic.TemplateView):
    template_name = "core/home.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        next_event = Event.objects.filter(start__gte=timezone.now(), event_type ='PUBLIC').first()
        #exemple de requête inverse many to many
        #rel = Location.objects.filter(customevents = next_custom_event ).select_related().first()
        #exemple de requête inverse one to many
        #print (next_custom_event.occurrence_set.first())
        #exemple de requête directe many to many
        #print (next_custom_event.locations.first())
        context = {'next_event': next_event}
        return context


class MemberhomePage(generic.TemplateView):
    template_name = "core/memberhome.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #prochaine répétition
        next_repet = Event.objects.filter(start__gte=timezone.now(), event_type ='REPET').first()
        #prochains concerts
        next_events = Event.objects.filter(start__gte=timezone.now()).exclude(event_type ='REPET')
        #derniers messages publiés
        publishedposts = Post.objects.filter(status=1).order_by('-created_on')[:10]
        context = {'next_repet': next_repet, 'next_events': next_events, 'publishedposts': publishedposts}
        return context


class InfoPage(generic.TemplateView):
    template_name = "core/info.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #prochaine répétition
        next_repet = Event.objects.filter(start__gte=timezone.now(), event_type ='REPET').first()
        context = {'event': next_repet}
        return context
    

class PhotoListView(generic.ListView):
    model = Photo


class VideoListView(generic.ListView):
    model = Video


def events_json(request):
    # Get all events
    events = Event.objects.all()
    # Create the fullcalendar json events list
    return HttpResponse(events_to_json(events),content_type='application/json')