# Generated by Django 4.2.4 on 2023-09-10 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beautician", "0010_alter_services_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="beautician",
            name="image",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
