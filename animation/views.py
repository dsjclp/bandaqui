from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.db.models import Q, Count
from .models import Piece
from .models import Instrument
from .models import Event
from .models import Eventinstrument
from .models import Participation
from .forms import ParticipationForm
from django.contrib import messages


class PieceListView(generic.ListView):
    model = Piece

def eventprogram(request, id):
    event = get_object_or_404(Event, pk=id)
    program = None
    return render(request, 'animation/event_program.html', {'event': event, 'program': program})

def eventdetail(request,id):
    event = get_object_or_404(Event, pk=id)
    instrumentpresences = Instrument.objects.annotate(num_participations=Count('instrumentparticipations',filter=Q(instrumentparticipations__event=event, instrumentparticipations__choice='OUI', instrumentparticipations__iswaiting=0)))
    presences = Participation.objects.filter(event=event, choice='OUI', iswaiting=0)
    absences = Participation.objects.filter(event=event, choice='NON')
    questions = Participation.objects.filter(event=event, choice='PEUT-ETRE')
    waitinglist = Participation.objects.filter(event=event, choice='OUI', iswaiting=1) 
    return render(request, 'animation/event_detail.html', {'event': event, 'instrumentpresences':instrumentpresences, 'presences': presences, 'absences': absences, 'questions': questions, 'waitinglist': waitinglist})

def save_participation_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            participation = form.save(commit=False)
            #suppression des anciennes inscriptions du même utilisateur pour le même événement
            oldparticipations = Participation.objects.filter(event=participation.event.pk, user=request.user)
            oldparticipations.delete()
            #enrichissement de l inscription
            participation.user=request.user
            participation.iswaiting=0
            # calcul du nb d instruments pour éventuelle mise en attente
            instrument = participation.instrument
            instrumentnb = Participation.objects.filter(event=participation.event.pk, instrument=instrument)
            instrumentnb = instrumentnb.count() + 1
            eventinstrument = Eventinstrument.objects.filter(event=participation.event.pk, instrument=instrument)
            instrumentnbmax = 99
            if eventinstrument :
                instrumentnbmax = eventinstrument[0].nbmax
            if instrumentnb > instrumentnbmax:
                participation.iswaiting = 1
            form.save() 
            data['form_is_valid'] = True
            instrumentpresences =  Instrument.objects.annotate(num_participations=Count('instrumentparticipations',filter=Q(instrumentparticipations__event=participation.event, instrumentparticipations__choice='OUI', instrumentparticipations__iswaiting=0)))
            presences = Participation.objects.filter(event=participation.event, choice='OUI', iswaiting=0)
            absences = Participation.objects.filter(event=participation.event, choice='NON')
            questions = Participation.objects.filter(event=participation.event, choice='PEUT-ETRE')
            waitinglist = Participation.objects.filter(event=participation.event, choice='OUI', iswaiting=1)
            data['html_event_detail'] = render_to_string('animation/participation_list.html', {
                'instrumentpresences': instrumentpresences, 'presences': presences, 
                'absences': absences, 'questions': questions, 'waitinglist': waitinglist,
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
    
def participation_create(request, id):
    if request.method == 'POST':
        form = ParticipationForm(request.user, id, request.POST)
    else:
        form = ParticipationForm(request.user, id)
        form.fields['event'].initial = id
    return save_participation_form(request, form, 'animation/participation_create.html')