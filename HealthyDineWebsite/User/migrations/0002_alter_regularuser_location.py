# Generated by Django 3.2.8 on 2022-04-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regularuser',
            name='location',
            field=models.CharField(max_length=10),
        ),
    ]