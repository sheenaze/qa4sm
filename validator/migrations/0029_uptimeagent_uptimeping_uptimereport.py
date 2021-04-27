# Generated by Django 3.1.3 on 2021-03-26 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validator', '0028_auto_20210216_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='UptimeAgent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('agent_key', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UptimePing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('agent_key', models.CharField(max_length=200)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UptimeReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('period', models.CharField(choices=[('DAILY', 'Daily'), ('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly'), ('YEARLY', 'Yearly')], max_length=10)),
                ('uptime_percentage', models.FloatField()),
            ],
        ),
    ]