# Generated by Django 2.1 on 2019-03-27 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validator', '0001_squashed_prep_for_new_schema_20190326_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='celerytask',
            name='id',
        ),
        migrations.AddField(
            model_name='celerytask',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]