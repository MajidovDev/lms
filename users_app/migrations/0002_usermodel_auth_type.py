# Generated by Django 4.2.2 on 2023-07-23 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='auth_type',
            field=models.CharField(blank=True, choices=[('via_email', 'via_email'), ('via_phone', 'via_phone')], max_length=31, null=True),
        ),
    ]
