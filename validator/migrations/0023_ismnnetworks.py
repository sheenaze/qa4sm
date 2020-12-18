# Generated by Django 3.0.8 on 2020-09-11 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validator', '0022_auto_20201110_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='ISMNNetworks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('continent', models.CharField(max_length=24)),
                ('country', models.CharField(max_length=60)),
                ('number_of_stations', models.IntegerField()),
                ('versions', models.ManyToManyField(related_name='network_version', to='validator.DatasetVersion')),
            ],
        ),
    ]