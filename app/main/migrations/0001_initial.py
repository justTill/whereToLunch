# Generated by Django 2.2.7 on 2020-04-12 15:54

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.model.models.restaurant


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_name', models.CharField(choices=[('website_name', 'website_name'), ('background_image', 'background_image'), ('openweathermap_api_key', 'openweathermap_api_key'), ('slack_app_api_key', 'slack_app_api_key'), ('slack_channel', 'slack_channel'), ('city_for_weather', 'city_for_weather'), ('website_url', 'website_url'), ('timezone', 'timezone')], default=[('website_name', 'website_name'), ('background_image', 'background_image'), ('openweathermap_api_key', 'openweathermap_api_key'), ('slack_app_api_key', 'slack_app_api_key'), ('slack_channel', 'slack_channel'), ('city_for_weather', 'city_for_weather'), ('website_url', 'website_url'), ('timezone', 'timezone')], max_length=50, unique=True)),
                ('string_property', models.CharField(blank=True, max_length=500, null=True)),
                ('image_property', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=12)),
                ('weather_group', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=150)),
                ('icon_id', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(max_length=100, unique=True)),
                ('restaurant_color', main.model.models.restaurant.ColorField(default='#ffffff', max_length=10)),
                ('restaurant_menu_link', models.URLField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_member_id', models.CharField(blank=True, max_length=100)),
                ('userImage', models.ImageField(upload_to='images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChoicesOfTheWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absenceFrom', models.DateField(default=datetime.date.today)),
                ('absenceTo', models.DateField(default=datetime.date.today)),
                ('reason', models.CharField(choices=[('absent', 'absent'), ('i am out', 'do not care'), ('do not care', 'i am out')], default=[('absent', 'absent'), ('i am out', 'do not care'), ('do not care', 'i am out')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
