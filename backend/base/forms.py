from django import forms
from django.forms import ModelForm, SplitDateTimeWidget, SplitDateTimeField
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Event, Organiser

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

class OrganiserRegistrationForm(UserCreationForm):
    """Form for organizer sign up"""

    class Meta:
        model = Organiser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email', 
            'password1', 
            'password2', 
        ]

class OrganiserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Organiser
        fields = [
            'first_name',
            'last_name',
            'phone',
            'profile_picture',
            'organiser_website',
            'organiser_birthday',
            'organiser_location',
            'organiser_bio',
        ]
        widgets = {
            'organiser_birthday': forms.DateInput(attrs={'type': 'date'}),
            'organiser_bio': forms.Textarea(attrs={'rows': 4}),
        }
