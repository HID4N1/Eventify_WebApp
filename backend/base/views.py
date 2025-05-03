from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
from .forms import EventForm
from django.contrib import messages

from django.views.decorators.http import require_http_methods

from .models import *


def Dashboard(request):
    # Fetch all events from the database
    events = Event.objects.all().select_related('organizer').prefetch_related('categories')
    customers = Customer.objects.all()
    TotalCustomers = customers.count()
    TotalEvents = events.count()
    completed_events = events.filter(status='completed').count()
    upcoming_events = events.filter(status='upcoming').count()
    cancelled_events = events.filter(status='cancelled').count()
    context = {
        'events': events,
        'customers': customers,
        'TotalCustomers': TotalCustomers,
        'TotalEvents': TotalEvents,
        'completed_events': completed_events,
        'upcoming_events': upcoming_events,
        'cancelled_events': cancelled_events,
        'page_title': 'Dashboard - Eventify',
        }
    return render(request, "base/dashboard.html", context)


def calendar(request):
    context = {
        'page_title': 'Calendar - Eventify',
    }
    return render(request, "base/calendar.html", context)


def event(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', 'all')
    date_filter = request.GET.get('date', '')

    events = Event.objects.all().select_related('organizer').prefetch_related('categories')

    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    if category_filter and category_filter != 'all':
        events = events.filter(categories__name__iexact=category_filter)

    if date_filter:
        events = events.filter(date__date=date_filter)

    categories = Category.objects.all()
    context = {
        'events': events,
        'categories': categories,
        'page_title': 'Events - Eventify',
        'search_query': search_query,
        'category_filter': category_filter,
        'date_filter': date_filter,
    }
    return render(request, "base/events.html", context)


def event_detail(request, pk):
    event = Event.objects.get(id=pk)
    customers = Customer.objects.filter(tickets__event=event).distinct()
    categories = event.categories.all()
    context = {
        'event': event,
        'customers': customers,
        'categories': categories,
        'page_title': 'Event Detail - Eventify',
    }
    return render(request, "base/event_detail.html", context)


def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            # Assign default organizer user to avoid NOT NULL constraint error
            try:
                default_organizer = User.objects.first()
            except User.DoesNotExist:
                default_organizer = None
            event.organizer = default_organizer
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event')
        else:
            messages.error(request, 'Error creating event. Please check the form.')
    context = {
        'form': form,
        'page_title': 'Create Event - Eventify',
    }

    return render(request, "base/event_form.html", context)


def update_event(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)
    if request.method == 'POST' :
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event')
    context = { 'form': form, 'page_title': 'Update Event - Eventify' }
    return render(request, "base/event_form.html", context)


def delete_event(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event')
    context = { 
        'event': event, 'page_title': 'Delete Event - Eventify'
     }
    return render(request, "base/delete_event.html", context)


def finance(request):
    context = {
        'page_title': 'Finance - Eventify',
    }
    return render(request, "base/finance.html", context)


def support(request):
    context = {
        'page_title': 'Support - Eventify',
    }
    return render(request, "base/support.html", context)
