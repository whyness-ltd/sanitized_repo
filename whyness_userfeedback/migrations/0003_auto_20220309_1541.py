# Generated by Django 3.2.12 on 2022-03-09 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_userfeedback', '0002_auto_20220309_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sweetspotconfidence',
            name='sort_order',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='sweetspotimpact',
            name='sort_order',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='sweetspotstrength',
            name='sort_order',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='sweetspotvalue',
            name='sort_order',
            field=models.SmallIntegerField(default=1),
        ),
    ]
