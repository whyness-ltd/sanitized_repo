# Generated by Django 3.2.11 on 2022-02-09 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_django', '0020_auto_20220209_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeattributes',
            name='description',
            field=models.TextField(default=''),
        ),
    ]