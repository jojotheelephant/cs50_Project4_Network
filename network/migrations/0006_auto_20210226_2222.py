# Generated by Django 3.1.5 on 2021-02-27 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210224_2103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='author',
        ),
    ]