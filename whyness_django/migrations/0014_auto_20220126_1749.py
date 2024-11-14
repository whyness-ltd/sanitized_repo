# Generated by Django 3.2.11 on 2022-01-26 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_django', '0013_alter_audio_transcript_s3'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('status', models.SmallIntegerField(default=1)),
                ('update_ip', models.GenericIPAddressField(default='::1')),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RunSQL(
            sql=("INSERT INTO whyness_django_authuser "
                "(uid, email, status, update_ip, update_date, create_date) "
                "VALUES ('xBdDyLsAAIZFsjGMbaRBBTrZang2', '', 1, '::1', NOW(), NOW());"
            ),
            reverse_sql=(
                'DELETE FROM whyness_django_authuser '
                'WHERE uid="xBdDyLsAAIZFsjGMbaRBBTrZang2";'
            )
        ),
        migrations.RemoveField(
            model_name='audio',
            name='update_user',
        ),
        migrations.AddField(
            model_name='audio',
            name='uid',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to='whyness_django.authuser'
            ),
            preserve_default=False,
        ),
    ]