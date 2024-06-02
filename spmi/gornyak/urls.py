from django.contrib import admin
from django.urls import path
from . import views
from .views import register_for_event, event_list, event_detail


urlpatterns = [
    path('', event_list, name='event_list'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    path('event/<int:event_id>/register/', register_for_event, name='register_for_event'),
]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Спортивные мероприятия"