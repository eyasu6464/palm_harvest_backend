# Generated by Django 4.2.7 on 2023-11-22 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('palmapp', '0005_remove_image_harvester_image_harvesterid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='harvesterid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
