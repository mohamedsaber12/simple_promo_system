# Generated by Django 3.1.3 on 2020-11-07 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]