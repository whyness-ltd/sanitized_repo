# Generated by Django 3.2.12 on 2022-02-23 13:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_django', '0023_alter_question_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='xref',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='AuthUser Reference'),
        ),
    ]
