# Generated by Django 4.2.4 on 2023-09-09 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beautician", "0004_alter_beautician_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="beautician",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
