from django.contrib import admin
from django.urls import path
from . import views
from .views import register_for_event, event_list


urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('events/', event_list, name='event_list'),
    path('event/<int:event_id>/register/', register_for_event, name='register_for_event'),
]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Спортивные мероприятия"