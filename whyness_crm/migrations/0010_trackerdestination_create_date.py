# Generated by Django 3.2.12 on 2022-02-28 10:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_crm', '0009_auto_20220228_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackerdestination',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]