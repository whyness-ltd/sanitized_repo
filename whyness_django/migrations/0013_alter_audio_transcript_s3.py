# Generated by Django 3.2.10 on 2022-01-17 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_django', '0012_auto_20220117_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='transcript_s3',
            field=models.TextField(default=''),
        ),
    ]