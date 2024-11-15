# Generated by Django 3.2.10 on 2022-01-17 18:24

from django.db import migrations, models
import whyness_django.models


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_django', '0011_audio_question'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audio',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='audio',
            name='transcript_json',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='audio',
            name='media',
            field=models.FileField(upload_to=whyness_django.models.file_field_callable),
        ),
        migrations.AlterField(
            model_name='audio',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Inactive'), (1, 'Active'), (2, 'Sent for transcription'), (3, 'Transcription in progress'), (4, 'Transcribed'), (5, 'Transcription failed'), (8, 'Deleted')], default=1),
        ),
    ]
