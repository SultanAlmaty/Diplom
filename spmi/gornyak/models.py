from django.db import models
from django.conf import settings

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'sport_table'
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'location_table'
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


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
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    sport_type = models.ForeignKey(Sport, on_delete=models.CASCADE)
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
        return f'{self.user} registered for {self.event}'

# Create your models here.
