# Generated by Django 3.2.16 on 2022-10-28 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20221028_0504'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Instructor',
            new_name='Teacher',
        ),
    ]