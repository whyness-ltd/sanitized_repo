# Generated by Django 3.2.9 on 2022-01-05 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_django', '0002_auto_20220104_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='title',
            field=models.CharField(default='', max_length=75, verbose_name='title'),
        ),
    ]
