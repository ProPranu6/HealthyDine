# Generated by Django 3.2.8 on 2022-05-06 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usr_id', models.IntegerField()),
                ('food_id', models.IntegerField()),
                ('quant', models.IntegerField()),
            ],
        ),
    ]
