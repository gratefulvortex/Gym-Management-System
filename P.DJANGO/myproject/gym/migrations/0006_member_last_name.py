# Generated by Django 5.0.3 on 2024-05-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0005_member_end_date_member_start_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='last_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]