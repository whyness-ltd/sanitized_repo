# Generated by Django 3.2.9 on 2022-01-07 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('whyness_timesheet', '0002_auto_20220107_1408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timeentry',
            options={'verbose_name': 'Timesheet entry', 'verbose_name_plural': 'Timesheet entries'},
        ),
        migrations.AddField(
            model_name='timeentry',
            name='strategy',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Business strategy'),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='update_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='timeentry_update_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='timeentry',
            constraint=models.UniqueConstraint(fields=('user', 'date'), name='unique_user_date'),
        ),
    ]