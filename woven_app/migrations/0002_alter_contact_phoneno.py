# Generated by Django 4.0.2 on 2022-08-21 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woven_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phoneno',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]