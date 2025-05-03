from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('login/', views.loginPage, name='login'),
    # path('register/', views.registerPage, name='register'),
    # path('logout/', views.logoutUser, name='logout'),
    path('', views.Dashboard, name='dashboard'),
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
