# Generated by Django 3.2.11 on 2022-02-09 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_django', '0019_auto_20220207_2050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profession',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'ordering': ['title']},
        ),
    ]