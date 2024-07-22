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
    EVENT_STATUS_CHOICES = [
        ('registration', 'Регистрация'),
        ('completed', 'Завершено'),
    ]

    EVENT_TYPE_CHOICES = [
        ('individual', 'Индивидуальное'),
        ('team', 'Командное'),
    ]

    name = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()  # Поле для начала мероприятия
    end_datetime = models.DateTimeField()  # Поле для конца мероприятия
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    sport_type = models.ForeignKey(Sport, on_delete=models.CASCADE)
    organizer = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=EVENT_STATUS_CHOICES, default='registration')
    registration_open = models.BooleanField(default=True)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='individual')
    link = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'event_table'
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['status','start_datetime']
        unique_together = ['name', 'start_datetime']

    def __str__(self):
        return self.name

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'user']
        verbose_name = 'Регистрация'
        verbose_name_plural = 'Регистрации'

    def __str__(self):
        return f'{self.user} registered for {self.event}'

# Create your models here.
