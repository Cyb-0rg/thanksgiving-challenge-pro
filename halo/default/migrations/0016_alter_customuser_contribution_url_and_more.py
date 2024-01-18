# Generated by Django 4.0.3 on 2023-11-30 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0015_customuser_country_code_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='contribution_url',
            field=models.TextField(max_length=120),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='expertise',
            field=models.TextField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='interest',
            field=models.TextField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_url',
            field=models.TextField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='project_url',
            field=models.TextField(max_length=120),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='team',
            field=models.TextField(blank=True, default='', max_length=40, null=True),
        ),
    ]