# Generated by Django 5.0.1 on 2024-06-02 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gornyak', '0008_event_link'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventregistration',
            options={'verbose_name': 'Регистрация', 'verbose_name_plural': 'Регистрации'},
        ),
        migrations.AlterField(
            model_name='event',
            name='end_datetime',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_datetime',
            field=models.DateField(),
        ),
    ]
