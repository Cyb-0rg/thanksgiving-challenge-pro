# Generated by Django 4.0.3 on 2023-11-24 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0009_merge_20231123_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_verification_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=18),
        ),
    ]
