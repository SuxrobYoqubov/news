# Generated by Django 4.2.4 on 2023-08-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
