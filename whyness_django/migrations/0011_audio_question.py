# Generated by Django 3.2.10 on 2022-01-14 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_django', '0010_alter_audio_transcribe_status_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='question',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='whyness_django.question'),
            preserve_default=False,
        ),
    ]