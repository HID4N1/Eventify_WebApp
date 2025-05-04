from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('organiser/register/', views.organizer_register, name='organiser_register'),
    path('logout/', views.logout, name='logout'),
    path('organiser/login/', views.organizer_login, name='organiser_login'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('calendar/', views.calendar, name='calendar'),
    path('event/', views.event, name='event'),
    path('finance/', views.finance, name='finance'),
    path('support/', views.support, name='support'),
    path('event_detail/<str:pk>/', views.event_detail, name='event-detail'),
    path('create_event/', views.create_event, name='create-event'),
    path('update_event/<str:pk>/', views.update_event, name='update-event'),
    path('delete_event/<str:pk>/', views.delete_event, name='delete-event'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

