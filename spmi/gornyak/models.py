from django.db import models
from django.conf import settings

class Event(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    SPORT_CHOICES = [
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('running', 'Running'),
        # Добавьте другие виды спорта по необходимости
    ]
    name = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()  # Поле для начала мероприятия
    end_datetime = models.DateTimeField()  # Поле для конца мероприятия
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sport_type = models.CharField(max_length=100, choices=SPORT_CHOICES)
    organizer = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='scheduled')

    class Meta:
        db_table = 'event_table'
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['start_datetime']
        unique_together = ['name', 'start_datetime']

    def __str__(self):
        return self.name

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'user']
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'

    def __str__(self):
        return f"{self.user.username} registered for {self.event.name}"

# Create your models here.
