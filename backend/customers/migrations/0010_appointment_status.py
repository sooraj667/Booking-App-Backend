# Generated by Django 4.2.4 on 2023-10-18 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0009_alter_review_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="status",
            field=models.CharField(default="Confirmed", max_length=200),
        ),
    ]
