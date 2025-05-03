from django import forms
from django.forms import ModelForm, SplitDateTimeWidget, SplitDateTimeField
from django.utils.translation import gettext_lazy as _
from .models import Event


class EventForm(ModelForm):
    date = SplitDateTimeField(
        widget=SplitDateTimeWidget(
            date_attrs={'type': 'date'},
            time_attrs={'type': 'time'}
        )
    )
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['organizer']
        widgets = {
            'date': SplitDateTimeWidget(
                date_attrs={'type': 'date'},
                time_attrs={'type': 'time'}
            ),
        }

  

 