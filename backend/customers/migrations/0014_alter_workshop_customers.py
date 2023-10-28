# Generated by Django 4.2.4 on 2023-10-22 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0013_workshopbooking"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workshop",
            name="customers",
            field=models.ManyToManyField(
                related_name="workshop", to="customers.customer"
            ),
        ),
    ]
