# Generated by Django 4.2.7 on 2023-11-22 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branchid', models.IntegerField(primary_key=True, serialize=False)),
                ('branchname', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('address_longitude', models.CharField(max_length=50)),
                ('address_latitude', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('imageid', models.IntegerField(primary_key=True, serialize=False)),
                ('image_created', models.DateTimeField()),
                ('image_uploaded', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.IntegerField(primary_key=True, serialize=False)),
                ('user_type', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('branchid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palmapp.branch')),
            ],
        ),
        migrations.CreateModel(
            name='PalmDetail',
            fields=[
                ('palmid', models.IntegerField(primary_key=True, serialize=False)),
                ('quality', models.CharField(max_length=50)),
                ('real', models.CharField(max_length=50)),
                ('predicted', models.BooleanField()),
                ('x1_coordinate', models.CharField(max_length=50)),
                ('y1_coordinate', models.CharField(max_length=50)),
                ('x2_coordinate', models.CharField(max_length=50)),
                ('y2_coordinate', models.CharField(max_length=50)),
                ('palm_image_uploaded', models.DateTimeField()),
                ('imageid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palmapp.image')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='harvester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palmapp.user'),
        ),
    ]