# Generated by Django 3.2.10 on 2022-01-13 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_django', '0009_audio_transcribe_status_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='transcribe_status_json',
            field=models.TextField(default=''),
        ),
    ]