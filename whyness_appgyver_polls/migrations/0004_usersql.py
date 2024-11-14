# Generated by Django 3.2.11 on 2022-02-19 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('whyness_appgyver_polls', '0003_auto_20220218_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSQL',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=100)),
                ('description', models.TextField(default='')),
                ('sql', models.TextField(default='')),
                ('status', models.SmallIntegerField(default=1)),
                ('update_ip', models.GenericIPAddressField(default='::1')),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
