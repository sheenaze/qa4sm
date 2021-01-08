# Generated by Django 3.1.3 on 2021-01-08 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('validator', '0025_statistics'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidationRun_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('copied_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copied_run', to='validator.validationrun')),
                ('original_run', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='original_run', to='validator.validationrun')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='validationrun',
            name='used_by',
            field=models.ManyToManyField(related_name='copied_runs', through='validator.ValidationRun_User', to=settings.AUTH_USER_MODEL),
        ),
    ]