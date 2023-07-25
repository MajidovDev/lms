# Generated by Django 4.2.2 on 2023-07-24 23:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions_app', '0003_questioncategorymodel_questionmodel_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='questioncategorymodel',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]