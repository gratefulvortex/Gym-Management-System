# Generated by Django 5.0.3 on 2024-04-09 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='tenure',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
