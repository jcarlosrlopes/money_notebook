# Generated by Django 3.0.5 on 2020-04-28 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_account_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oncreditsale',
            name='receipt',
            field=models.ImageField(blank=True, upload_to='sales/images'),
        ),
    ]