# Generated by Django 3.1.2 on 2024-11-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='seat',
            constraint=models.UniqueConstraint(fields=('bus_id', 'seat_code'), name='unique_bus_seat_code'),
        ),
    ]
