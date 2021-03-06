# Generated by Django 2.2.7 on 2020-04-15 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200415_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slack_member_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='userImage',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
