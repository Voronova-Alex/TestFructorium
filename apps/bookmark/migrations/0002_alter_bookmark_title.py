# Generated by Django 4.2.1 on 2023-08-20 11:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookmark", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookmark",
            name="title",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
