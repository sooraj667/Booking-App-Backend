# Generated by Django 4.2.4 on 2023-10-13 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0006_appointment_booked_timing_appointment_service"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="wallet_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
