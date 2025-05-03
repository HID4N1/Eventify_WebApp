from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    """User model for event organizers"""
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.username
    

class Category(models.Model):
    """Event categories"""
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    """Event model for organizers"""
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    main_image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.organizer.username}"

class Customer(models.Model):
    """Ticket purchasing customers"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Ticket(models.Model):

    """Event tickets with different types"""
    TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('vip', 'VIP'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='regular')
    purchase_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    
    def __str__(self):
        return f"{self.ticket_type} ticket for {self.event.title}"
