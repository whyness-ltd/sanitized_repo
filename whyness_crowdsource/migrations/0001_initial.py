# Generated by Django 3.2.12 on 2022-03-28 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('whyness_django', '0026_alter_audio_status'),
        ('whyness_userfeedback', '0004_auto_20220309_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.SmallIntegerField(default=0)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='whyness_django.authuser')),
            ],
        ),
        migrations.CreateModel(
            name='StoryGrant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('update_ip', models.GenericIPAddressField(default='::1')),
                ('is_granted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='whyness_django.authuser')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewSweetSpot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField(default='::1')),
                ('valueother', models.CharField(blank=True, default='', max_length=100)),
                ('strengthother', models.CharField(blank=True, default='', max_length=100)),
                ('impactother', models.CharField(blank=True, default='', max_length=100)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('impact1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotimpact')),
                ('impact2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotimpact')),
                ('impact3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotimpact')),
                ('impactconfidence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotconfidence')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whyness_crowdsource.review')),
                ('strength1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotstrength')),
                ('strength2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotstrength')),
                ('strength3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotstrength')),
                ('strengthconfidence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotconfidence')),
                ('useragent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='whyness_django.useragent')),
                ('value1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotvalue')),
                ('value2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotvalue')),
                ('value3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotvalue')),
                ('valueconfidence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='whyness_userfeedback.sweetspotconfidence')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ReviewStories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whyness_crowdsource.review')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whyness_django.audio')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewReviewer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField(default='')),
                ('status', models.SmallIntegerField(default=0)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='whyness_crowdsource.review')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='whyness_django.authuser')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewFeedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField(default='')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whyness_crowdsource.review')),
            ],
        ),
    ]
