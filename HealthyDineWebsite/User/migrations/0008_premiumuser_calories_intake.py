# Generated by Django 3.2.8 on 2022-05-07 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_auto_20220505_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='premiumuser',
            name='calories_intake',
            field=models.FloatField(default=2500),
        ),
    ]
