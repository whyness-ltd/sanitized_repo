# Generated by Django 3.2.12 on 2022-02-21 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_crm', '0002_usersql'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersql',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
        migrations.AddField(
            model_name='usersql',
            name='sql_select',
            field=models.CharField(default='SELECT *', max_length=100),
        ),
    ]
