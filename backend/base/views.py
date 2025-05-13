from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import PasswordChangeForm
from .forms import EventForm, OrganiserRegistrationForm, UserSettingsForm, OrganiserProfileUpdateForm
from .decorators import organizer_required

from .models import *

def home(request):
        return render(request, 'base/home.html', {'page_title': 'Home - Eventify'})

@organizer_required
def Dashboard(request):
    """View for the dashboard"""
    if not request.user.is_authenticated or not hasattr(request.user, 'username'):
        return redirect('login')  # Only organizers can access
    events = Event.objects.filter(organizer=request.user).select_related('organizer').prefetch_related('categories')
    customers = Customer.objects.filter(tickets__event__organizer=request.user).distinct()
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

@organizer_required
def event(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', 'all')
    date_filter = request.GET.get('date', '')

    events = Event.objects.filter(organizer=request.user).select_related('organizer').prefetch_related('categories')

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

@organizer_required
def event_detail(request, pk):
    event = Event.objects.get(id=pk, organizer=request.user)
    customers = Customer.objects.filter(tickets__event=event).distinct()
    categories = event.categories.all()
    context = {
        'event': event,
        'customers': customers,
        'categories': categories,
        'page_title': 'Event Detail - Eventify',
    }
    return render(request, "base/event_detail.html", context)

@organizer_required
def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
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

@organizer_required
def update_event(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event')
    context = {'form': form, 'page_title': 'Update Event - Eventify'}
    return render(request, "base/event_form.html", context)

@organizer_required
def delete_event(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event')
    context = {
        'event': event,
        'page_title': 'Delete Event - Eventify'
    }
    return render(request, "base/delete_event.html", context)

@organizer_required
def finance(request):
    context = {
        'page_title': 'Finance - Eventify',
    }
    return render(request, "base/finance.html", context)

@organizer_required
def support(request):
    context = {
        'page_title': 'Support - Eventify',
    }
    return render(request, "base/support.html", context)

@organizer_required
def settings(request):
    user = request.user
    active_tab = request.GET.get('tab', 'general')
    if request.method == 'POST':
        if 'update_settings' in request.POST:
            user_settings_form = UserSettingsForm(request.POST, instance=user)
            if user_settings_form.is_valid():
                user_settings_form.save()
                messages.success(request, 'Settings updated successfully.')
                return redirect('/settings/?tab=general')
            else:
                messages.error(request, 'Please correct the errors in the settings form.')
            password_form = PasswordChangeForm(user)
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in
                messages.success(request, 'Password updated successfully.')
                return redirect('/settings/?tab=privacy')
            else:
                messages.error(request, 'Please correct the errors in the password form.')
            user_settings_form = UserSettingsForm(instance=user)
    else:
        user_settings_form = UserSettingsForm(instance=user)
        password_form = PasswordChangeForm(user)

    context = {
        'page_title': 'Settings - Eventify',
        'active_tab': active_tab,
        'user_settings_form': user_settings_form,
        'password_form': password_form,
    }
    return render(request, "base/settings.html", context)

from .forms import EventForm, OrganiserRegistrationForm, UserSettingsForm

@organizer_required
def profile(request):
    if request.method == 'POST':
        form = OrganiserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OrganiserProfileUpdateForm(instance=request.user)
    context = {
        'page_title': 'Profile - Eventify',
        'form': form,
    }
    return render(request, "base/profile.html", context)

def organizer_register(request):
    """View for organizer registration"""
    if request.method == 'POST':
        form = OrganiserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('organiser_login')
    else:
        form = OrganiserRegistrationForm()
    return render(request, 'base/register.html', {'form': form})

def organizer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['app_user_id'] = user.id
            return redirect('dashboard')
        else:
            return render(request, 'base/login.html', {'error': 'Invalid credentials'})
    return render(request, 'base/login.html')

def logout(request):
    if request.method == 'POST':
        if 'app_user_id' in request.session:
            del request.session['app_user_id']
        auth_logout(request)
        return redirect('home')
    return render(request, 'base/home.html')


from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .models import Event
from datetime import datetime, timedelta

@organizer_required
def analytics(request):
    """View for analytics dashboard"""
    if not request.user.is_authenticated:
        return redirect('login')

    # Get date range from request or use default (last 30 days)
    date_range = request.GET.get('range', '30d')
    end_date = timezone.now()
    
    if date_range == '7d':
        start_date = end_date - timedelta(days=7)
    elif date_range == '30d':
        start_date = end_date - timedelta(days=30)
    elif date_range == '90d':
        start_date = end_date - timedelta(days=90)
    elif date_range == '12m':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)

    # Event status breakdown
    status_data = (
        Event.objects.filter(organizer=request.user)
        .values('status')
        .annotate(count=Count('status'))
        .order_by('status')
    )

    # Performance over time (events created)
    performance_data = []
    current_date = start_date
    
    while current_date <= end_date:
        day_events = Event.objects.filter(
            organizer=request.user,
            created_at__date=current_date
        ).count()
        
        performance_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'events': day_events,
        })
        
        current_date += timedelta(days=1)

    context = {
        'page_title': 'Analytics - Eventify',
        'status_data': list(status_data),
        'performance_data': performance_data,
        'date_range': date_range,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
    
    return render(request, 'base/analytics.html', context)