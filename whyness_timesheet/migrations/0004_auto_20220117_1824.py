# Generated by Django 3.2.10 on 2022-01-17 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whyness_timesheet', '0003_auto_20220107_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeentry',
            name='admin_pmo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Admin PMO Financial - do not use'),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='comms_marketing',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Market / Customer Research & Engagement, & Strategy'),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='design_architecture',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Solution Design and Development'),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='functional',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Functional - do not use'),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='hr_recruitment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Recruitment'),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='product_development',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Product development (tech) - do not use'),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='statutory_holiday',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Statutory holiday - do not use'),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='strategy',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Business strategy - do not use'),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='sustainability',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Sustainability - do not use'),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='user_research',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='User research and testing'),
        ),
    ]
