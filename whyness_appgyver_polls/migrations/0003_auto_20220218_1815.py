# Generated by Django 3.2.11 on 2022-02-18 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_appgyver_polls', '0002_auto_20220214_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='dreamjob',
            name='professionother',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='dreamjob',
            name='roleother',
            field=models.CharField(default='', max_length=100),
        ),
    ]