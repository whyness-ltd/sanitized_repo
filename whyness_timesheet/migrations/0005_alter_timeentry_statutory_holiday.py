# Generated by Django 3.2.11 on 2022-02-02 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_timesheet', '0004_auto_20220117_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeentry',
            name='statutory_holiday',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Bank holiday'),
        ),
    ]