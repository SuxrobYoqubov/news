# Generated by Django 4.2.4 on 2023-10-18 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]