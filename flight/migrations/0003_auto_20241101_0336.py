# Generated by Django 3.1.2 on 2024-10-31 21:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0002_auto_20241101_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='seat_class',
            field=models.CharField(choices=[('ECONOMY', 'Economy'), ('FIRST', 'First'), ('SLEEPER', 'Sleeper')], max_length=20),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='booking_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seat_class',
            field=models.CharField(choices=[('ECONOMY', 'Economy'), ('FIRST', 'First'), ('SLEEPER', 'Sleeper')], max_length=20),
        ),
    ]
