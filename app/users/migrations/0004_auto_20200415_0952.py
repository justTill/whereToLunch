# Generated by Django 2.2.7 on 2020-04-15 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200415_0950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='userImage',
            new_name='user_image',
        ),
    ]
