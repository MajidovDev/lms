# Generated by Django 4.2.2 on 2023-07-25 00:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions_app', '0004_questioncategorymodel_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questioncommentlikemodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='questioncommentmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='questionmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL),
        ),
    ]
