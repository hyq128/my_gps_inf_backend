# Generated by Django 4.2.2 on 2024-05-14 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccelerometerInf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acc_x', models.FloatField(default=0.0)),
                ('acc_y', models.FloatField(default=0.0)),
                ('acc_z', models.FloatField(default=0.0)),
                ('device', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='BlueToothInf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_device', models.CharField(default='', max_length=150)),
                ('device', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='LocationInf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.FloatField(default=0.0)),
                ('latitude', models.FloatField(default=0.0)),
                ('device', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.DeleteModel(
            name='UserInf',
        ),
    ]
