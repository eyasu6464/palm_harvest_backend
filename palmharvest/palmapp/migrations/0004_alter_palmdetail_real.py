# Generated by Django 4.2.7 on 2023-12-08 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palmapp', '0003_passwordreset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palmdetail',
            name='real',
            field=models.BooleanField(),
        ),
    ]