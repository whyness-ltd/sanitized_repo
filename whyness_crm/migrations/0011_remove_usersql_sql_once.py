# Generated by Django 3.2.12 on 2022-03-14 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_crm', '0010_trackerdestination_create_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersql',
            name='sql_once',
        ),
    ]
