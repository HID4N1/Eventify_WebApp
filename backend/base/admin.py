from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Organiser)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Ticket)