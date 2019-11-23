from django import forms
from .models import Participation
from .models import Instrument


class ParticipationForm(forms.ModelForm):

    class Meta:
        model = Participation
        fields = ['event','choice','instrument',]
        widgets = {'event': forms.HiddenInput()}
     

    def __init__(self, user, event, *args, **kwargs):
        super(ParticipationForm, self).__init__(*args, **kwargs)
        PARTICIPATION_CHOICES = [
            ('OUI', 'J y serai'),
            ('NON', 'Je n y serai pas'),
            ('PEUT-ETRE', 'Je ne suis pas sûr'),  
        ]
        user_instruments = Instrument.objects.filter(instrumentuserinstruments__user=user)
        if user_instruments :
            self.fields['instrument'].queryset = user_instruments
            self.fields['instrument'].initial = user_instruments[0]
        else :
            self.fields['instrument'].queryset = Instrument.objects.filter()
            self.fields['instrument'].initial = Instrument.objects.filter()[0]
        self.fields['event'].label = ''
        self.fields['choice'].queryset = PARTICIPATION_CHOICES
        self.fields['choice'].label = 'Votre choix'
        self.fields['choice'].initial = 'OUI'