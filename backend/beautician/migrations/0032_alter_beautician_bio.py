# Generated by Django 4.2.4 on 2023-10-19 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beautician", "0031_alter_beautician_bio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="beautician",
            name="bio",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
