# Generated by Django 3.2.9 on 2022-01-04 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('whyness_django', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('hostip', models.GenericIPAddressField(null=True)),
                ('hostname', models.CharField(blank=True, max_length=500)),
                ('useragent', models.CharField(blank=True, max_length=500)),
                ('errorcode', models.TextField(blank=True, verbose_name='Error code')),
                ('errormessage', models.TextField(blank=True, verbose_name='Error message')),
            ],
        ),
        migrations.CreateModel(
            name='UserAgent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('useragent', models.CharField(blank=True, max_length=500, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='audio',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='audio',
            name='update_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
