# Generated by Django 3.2.15 on 2022-09-27 16:51

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('whyness_django', '0026_alter_audio_status'),
    ]

    sql_create_trackerlog = """
    CREATE VIEW whyness_django_trackerlog_view AS
    SELECT
        log.id AS id,
        au.id AS user_id,
        au.email AS email,
        item.title,
        item.description,
        log.ip,
        ua.useragent,
        log.method,
        log.create_date
    FROM whyness_django_trackerlog AS log
    INNER JOIN whyness_django_trackeritem AS item
    ON log.item_id = item.id
    INNER JOIN whyness_django_useragent AS ua
    ON log.useragent_id = ua.id
    INNER JOIN whyness_django_authuser AS au
    ON log.user_id = au.id
    """

    sql_drop_trackerlog = "DROP VIEW whyness_django_trackerlog_view"

    operations = [
        migrations.RunSQL(
            sql=[sql_create_trackerlog],
            reverse_sql=[sql_drop_trackerlog],
        )
    ]
